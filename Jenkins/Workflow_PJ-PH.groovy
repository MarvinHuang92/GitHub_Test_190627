//#### 		JENKINS WORKFLOW FOR PJ_PH		    ###########

import groovy.transform.Field
@Library('script-checkout-helper') _

String toolsBranch = env.SCRIPT_BRANCH
String directoryToScripts = checkoutScripts("${toolsBranch}")

libraryFunctions = loadFromScriptDirectory(directoryToScripts, 'functions/functions.groovy')
libraryFunctions_PJPH = loadFromScriptDirectory(directoryToScripts, 'functions/functions_PJPH.groovy')
stage_build = loadFromScriptDirectory(directoryToScripts, 'stages/build.groovy')
stage_buildcmake = loadFromScriptDirectory(directoryToScripts, 'stages/buildCMake.groovy')
stage_smoketest = loadFromScriptDirectory(directoryToScripts, 'stages/smokeTest.groovy')
stage_userScripts = loadFromScriptDirectory(directoryToScripts, 'stages/userScripts.groovy')
stage_bctCheck = loadFromScriptDirectory(directoryToScripts, 'stages/cmake/bctCheck.groovy')
email_notification = loadFromScriptDirectory(directoryToScripts, 'functions/email_notification.groovy')

gitSpecifier = env.BRANCH_OR_COMMIT_TO_BUILD
mergeBeforeBuild = env.MERGE_WITH_BRANCH

notifyBitbucket = getBuildParameter('NOTIFY_BITBUCKET', false)

archiveBuildArtifacts = getBuildParameter('ARCHIVE_BUILD_ARTIFACTS', false)

currentBuild.displayName = "#${BUILD_NUMBER}, ${gitSpecifier}"
sha = libraryFunctions.getCommitNotificationFromLog()
NodeLabel = env.NODE_LABEL
repoUrl = env.REPO_URL

additionalParams = params.ADDITIONAL_PARAMS
if (additionalParams?.trim()){
    libraryFunctions.setAdditionalParams(additionalParams)
}

boolean automaticallyTriggered = (sha.length() > 0) //When a build is triggered automatically from a commit/PR from Bitbucket, notify the status to Bitbucket server

if (automaticallyTriggered) {
    gitSpecifier = sha
}
notifyBitbucketShas = libraryFunctions.getNotifyBitbucketShas()

if (automaticallyTriggered) {
    libraryFunctions.notifyBitbucket(notifyBitbucketShas, notifyBitbucket)
    currentBuild.description = "Automated Build - ${gitSpecifier}"
    try {
        WorkFlow()
        libraryFunctions.signalPipelineSuccess(notifyBitbucketShas, notifyBitbucket)
    } catch(err) {
        libraryFunctions.signalPipelineError(notifyBitbucketShas, notifyBitbucket)
        email_notification.sendNotification()
        throw err
    }
} else {
    libraryFunctions.notifyBitbucket(notifyBitbucketShas, notifyBitbucket)

    String startedBy = libraryFunctions.getStartedByFromLog()
    currentBuild.description = "Manual Config Update (${startedBy})"
    email_notification.sendNotificationManualTriggerStartJob() // Notify the user that job has started

    try {
        WorkFlow()
        libraryFunctions.signalPipelineSuccess(notifyBitbucketShas, notifyBitbucket)
    } catch(err) {
        libraryFunctions.signalPipelineError(notifyBitbucketShas, notifyBitbucket)
        throw err
    } finally{
        email_notification.sendNotification() // Notify the user that job has completed(success/failure)
    }
}

def WorkFlow()
{
    try
    {
        node(NodeLabel)
        { libraryFunctions.withCommonWorkspace {

            currentBuild.description = currentBuild.description+"<br>Build Node: ${env.NODE_NAME}"

            def variantsList = libraryFunctions_PJPH.getListOfAppVars(env.VARIANT_LIST)

            stage('Checkout')
            {
                libraryFunctions.checkoutSources(repoUrl, gitSpecifier)
            }

            if (env.FQM_check == 'true')
            {
                stage_userScripts.FQM_check()
            }

            if (env.GEN_SCOM == 'true')
            {
                stage_build.GEN_SCOM()
            }

            /*Run only BCT build test in another node.No Target build OR CMake build included.
            This condition is handled in a seperate pipeline job and the parameter "BCT_TEST" is SET only in that pipeline job.
            The pipeline includes sub stages 'Create Build Setup' and subsequent BCT Test steps for all the available variants.
            */
            if (env.BCT_TEST == 'true')
            {
                stage_bctCheck.buildBCT()
            }

            parallel (
                BUILD : {
                // Run the mandatory FLIST build. Includes sub stages CREATE BUILD SETUP, INIT RUN, TARGET RUN for all the avialable variants.
                    if (env.TARGET_BUILD == 'true')
                    {
                        stage_build.build()
                    }
                },

                SELENA_BUILD : {
                /* Runs the Selena build parallel with Target Build. Currently disabled since it takes more time to execute.
                Add libraryFunctions.withShortWorkspace while enabling for shorter workspace during Selena build
                */
                    if (env.SELENA_BUILD == 'true')
                    {
                        stage_build.selena_build()
                    }
                }
            )

            if (env.RESOURCE_CALC == 'true')
            {
                stage_userScripts.ResourceCalc()
            }

            // Run various build steps for the different variants
            for (int i = 0; i < variantsList.size(); i++)
            {
                def appVar = variantsList[i]
                def UNIQUE_VARIANT_NAME = libraryFunctions_PJPH.getVariant(appVar)
                def BuildDir = "build\\${UNIQUE_VARIANT_NAME.toUpperCase()}"

                // Run the FLIST build. Includes sub stages CREATE BUILD SETUP, INIT RUN, TARGET RUN for all the avialable variants
                if ( env.CMAKE_VARIANT_LIST != "" && env.CMAKE_VARIANT_LIST != null )
                {
                    stage_buildcmake.CmakebuildVariant(UNIQUE_VARIANT_NAME)
                }

                if (env.SMOKETEST == 'true')
                {
                    stage('Prepare Smoketest')
                    {
                        stage_smoketest.prepareSmokeTest(appVar,libraryFunctions_PJPH)
                    }

                    stage('Stashing Files')
                    {
                        stage_smoketest.StashBuildFiles(BuildDir)
                    }
                }
            }
        }}

        if (env.SMOKETEST == 'true')
        {
            echo "Checking out the repo in test node"
            NodeLabel_hw = env.NODE_LABEL_HW

            node(NodeLabel_hw)
            { libraryFunctions.withCommonWorkspace {

                currentBuild.description = currentBuild.description+"<br>Test Node: ${env.NODE_NAME}"

                def variantsList = libraryFunctions_PJPH.getListOfAppVars(env.VARIANT_LIST)
                def appVar = variantsList[0]
                def UNIQUE_VARIANT_NAME = libraryFunctions_PJPH.getVariant(appVar)
                def BuildDir = "build//${UNIQUE_VARIANT_NAME.toUpperCase()}"
                def ARTEFACT_RELEASE_DIR = "${BuildDir}//release"

                stage('Test Node Checkout')
                {
                    stage_smoketest.SmokeTestCheckout(repoUrl, gitSpecifier)
                }

                stage('Unstashing Files')
                {
                    stage_smoketest.UnstashBuildFiles(BuildDir)
                }

                stage('VMC MTC GEN&VER')
                {
                if (env.CREATE_VMC_MTC_APPL_CONTAINER == 'true')
                    {
                        currentBuild.description = currentBuild.description+"<br>VMC MTC BUILD & CONSISTENCY CHECK ENABLED!"
                        echo "VMC MTC BUILD & CONSISTENCY CHECK!"

                        stage_smoketest.VMC_MTC_BUILD(appVar,libraryFunctions_PJPH)
                    }
                    else
                    {
                        currentBuild.description = currentBuild.description+"<br>VMC MTC BUILD & CONSISTENCY CHECK DISABLED!"
                        echo "VMC MTC BUILD & CONSISTENCY CHECK DISABLED!"

                    }
                }

                stage('Generate A2L Files')
                {
                    stage_smoketest.runCreateCppA2Lfiles(appVar,libraryFunctions_PJPH)
                }

                stage('Smoke Test')
                {
                    try
                    {
                        stage_smoketest.smokeTest(appVar,libraryFunctions_PJPH)
                    }
                    catch(e)
                    {
                        echo "[Error  ] A failure has occured..."
                        echo "[Info   ] Trying to archive SMOKE_TEST_RESULTS.zip before continuing..."
                        libraryFunctions.publishFilesToJenkins("${ARTEFACT_RELEASE_DIR}//**.zip",true)
                        throw e
                    }
                }

                stage('VMC MTC APPL')
                {
                    if (env.CREATE_VMC_MTC_APPL_CONTAINER == 'true')
                    {
                        currentBuild.description = currentBuild.description+"<br>Creation of VMC MTC Offline calibration container enabled !"
                        echo "Creation of VMC MTC Offline calibration container enabled!"

                        stage_smoketest.creatingVMC_MTC_APPL_CONTAINER(appVar,libraryFunctions_PJPH)
                    }
                    else
                    {
                        currentBuild.description = currentBuild.description+"<br>Creation of VMC MTC Offline calibration container disabled !"
                        echo "Creation of VMC MTC Offline calibration container disabled!"

                    }
                }

                stage('Release Dir Zip')
                {
                    stage_smoketest.creatingReleaseDirZip(appVar,libraryFunctions_PJPH)
                }
            }}
        }
        if (archiveBuildArtifacts) {
            libraryFunctions.publishArtifactoryLinks()
        }
    }
    catch (Throwable exception)
    {
        throw exception
    }
}
