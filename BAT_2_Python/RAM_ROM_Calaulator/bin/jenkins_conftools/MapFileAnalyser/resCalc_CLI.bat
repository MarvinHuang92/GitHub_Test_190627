@echo off
title resCalc_CLI
setlocal

REM Support for ResCalc tool: Denes.Kraszulyak@hu.bosch.com
REM
REM #   Parameters:             Description:
REM #   %1: Variant String      This String is necessary to declare if a DASyBase or DASyENH Software build is active. Following options are possible:
REM         jlr_my20_base       (for DASy Base)
REM         jlr_my20_enh        (for DASy_ENH)
REM #   %2: Network iteration
REM         {NI5, NI6, NI7(, NI8)}
REM #   %3: Additional option
REM         --old               (for handling of legacy repos)
echo resCalc_CLI.bat - start

echo ************************************************************
echo resCalc_CLI
echo Project must be compiled first - x.map file must exist

echo ############################################################

echo Author: Divya Vemparala Guruswamy(CC-DA/ESI2)
echo Date: 30.11.2017
echo Changed: 21.12.2017 Ulrich Koerber(CC-DA/EAD1)
echo Changed: 12.02.2018 Alexander Ehni(CC-DA/EAD1)
echo Changed: 09.03.2018 Alexander Ehni(CC-DA/EAD5)
echo Changed: 19.03.2018 Alexander Ehni(CC-DA/EAD5)
echo Changed: 23.03.2018 Alexander Ehni(CC-DA/EAD5)
echo Changed: 06.09.2018 Ulrich Koerber(CC-DA/EAD5)
echo Changed: 04.10.2018 Ulrich Koerber(CC-DA/EAD5)
echo Changed: 29.10.2018 Nithish Shetty Bare(CC-AD/ESW3)
echo Changed: 15.02.2019 Benjamin Staab(CC-DA/EAD1)
echo Changed: 27.03.2019 Chirag G(RBEI/ESX1)
echo Changed: 17.07.2019 Roshitha Babu G(RBEI/ESX3)
echo Changed: 20.08.2019 HUANG Marvin(CC-DA/EAY2-CN)
echo ************************************************************
REM Check parameter preconditions
if "%1" == "" (
  echo "No variant code as parameter 1 (jlr_my20_base or jlr_my20_enh or APL_BJEV or APL_GAC) available!"
  goto EXIT_ON_ERROR
)
if /i "%1" == "jlr_my20_base" goto SET_ROOT
if /i "%1" == "jlr_my20_enh" goto SET_ROOT
if /i "%1" == "APL_BJEV" goto SET_ROOT
if /i "%1" == "APL_GAC" goto SET_ROOT
echo "Variant code as parameter 1 has to be jlr_my20_base or jlr_my20_enh or APL_BJEV or APL_GAC! For passing info about network iteration use parameter 2."
goto EXIT_ON_ERROR

:SET_ROOT
REM Get drive, path of root_parent
for %%A in ("%~dp0\..\..") do set "root_parent=%%~fA"

REM Set suitable parameters for NI variants
if /i "%2" == "NI5" goto NI5
if /i "%2" == "NI6" goto NI6
if /i "%2" == "NI7" goto NI7
if /i "%2" == "CMP" goto CMP
if /i "%2" == "GAC" goto GAC
rem if /i "%2" == "NI8" goto NI8
rem echo "No, or not suitable, network iteration as parameter 2 (NI5, NI, NI7 or NI8) available."
echo "No, or not suitable, network iteration as parameter 2 (NI5, NI6 or NI7) available."
goto EXIT_ON_ERROR

:NI5
set NETWORK_ITERATION=%2
if /i "%3" == "--old" (set VARIANT_CODE=%1) else (set VARIANT_CODE=DASY_%1_NI5)
if /i "%3" == "--old" (
  set mapName=%root_parent%\build_cmake\%VARIANT_CODE%\exec\%VARIANT_CODE%.map
  set reportPath=%root_parent%\build_cmake\%VARIANT_CODE%
) else (
  set mapName=%root_parent%\generatedFiles\%VARIANT_CODE%\exec\%VARIANT_CODE%.map
  set reportPath=%root_parent%\generatedFiles\%VARIANT_CODE%
)
set layout=%root_parent%\jenkins_conftools\MapFileAnalyser\memory_layout_NI5.xml
set ghsPath=C:\TCC\Tools\greenhills_ifx\comp_201715_1fp_WIN\decode.exe
goto COMMON_SETUP

:NI6
set NETWORK_ITERATION=%2
set VARIANT_CODE=DASY_%1
if /i "%3" == "--old" (
  set mapName=%root_parent%\generatedFiles\%VARIANT_CODE%\%VARIANT_CODE%.map
) else (
  set mapName=%root_parent%\generatedFiles\%VARIANT_CODE%\exec\%VARIANT_CODE%.map
)
set layout=%root_parent%\jenkins_conftools\MapFileAnalyser\memory_layout.xml
set ghsPath=C:\TCC\Tools\greenhills_ifx\comp_201815_1fp_WIN64\decode.exe
set reportPath=%root_parent%\generatedFiles\%VARIANT_CODE%
goto COMMON_SETUP

:NI7
set NETWORK_ITERATION=%2
set VARIANT_CODE=DASY_%1
set mapName=%root_parent%\generatedFiles\%VARIANT_CODE%\exec\%VARIANT_CODE%.map
set layout=%root_parent%\jenkins_conftools\MapFileAnalyser\memory_layout.xml
set ghsPath=C:\TCC\Tools\greenhills_ifx\comp_201815_1fp_WIN64\decode.exe
set reportPath=%root_parent%\generatedFiles\%VARIANT_CODE%
goto COMMON_SETUP

:CMP
set NETWORK_ITERATION=%2
set VARIANT_CODE=DASY_%1
SET mapName=%root_parent%\generatedFiles\%VARIANT_CODE%\exec\%VARIANT_CODE%.map
if not exist %mapName% (
	echo Error: File %mapName% missing
 	pause
	exit -1
)
SET layout=%root_parent%\jenkins_conftools\MapFileAnalyser\memory_layout_CMP.xml
SET ghsPath=C:\TCC\Tools\greenhills_ifx\comp_201715_1fp_WIN\decode.exe
SET reportPath=%root_parent%\generatedFiles\%VARIANT_CODE%
goto COMMON_SETUP

:GAC
set NETWORK_ITERATION=%2
set VARIANT_CODE=DASY_%1
SET mapName=%root_parent%\generatedFiles\%VARIANT_CODE%\exec\%VARIANT_CODE%.map
if not exist %mapName% (
	echo Error: File %mapName% missing
 	pause
	exit -1
)
SET layout=%root_parent%\jenkins_conftools\MapFileAnalyser\memory_layout_CMP.xml
SET ghsPath=C:\TCC\Tools\greenhills_ifx\comp_201815_4fp_WIN64\decode.exe
SET reportPath=%root_parent%\generatedFiles\%VARIANT_CODE%
goto COMMON_SETUP

:NI8
rem ToDo.
goto COMMON_SETUP

:COMMON_SETUP
set resCalcPath=ghs_map_resourcecalculator_release
set reportXML=%reportPath%\%VARIANT_CODE%_report.xml



:EXECUTE
REM Print variables
echo # Variables in use #
echo.
echo root_parent: %root_parent%
echo.
echo variant: %VARIANT_CODE%
echo.
echo networkIteration: %NETWORK_ITERATION% %3
echo.
echo layout: %layout%
echo.
echo ghsPath: %ghsPath%
echo.
echo reportPath: %reportPath%
echo.
echo resCalcPath: %resCalcPath%
echo.

REM Clean old output
if exist %reportXML% del %reportXML%

REM Check for input files
if not exist %mapName% (
    echo Error: File %mapName% missing
    goto EXIT_ON_ERROR
)

REM Run calculations
echo ***************************
echo Calling resCalcAurixCLI.exe
echo ***************************
echo.

cd %root_parent%\jenkins_conftools\MapFileAnalyser\%resCalcPath%
call resCalcAurixCLI.exe -mapName="%mapName%" -layout="%layout%" -ghsPath="%ghsPath%" -reportPath="%reportPath%"

REM Check for output files
if exist %reportXML% (
    echo OK: report.xml generated -see: %reportXML%
    goto EXIT_ON_SUCCESS
) else (
    echo Error: report.xml generation failed
    goto EXIT_ON_ERROR
)

:EXIT_ON_SUCCESS
echo resCalc_CLI.bat - exit on SUCCESS
endlocal
exit /b 0

:EXIT_ON_ERROR
echo resCalc_CLI.bat - exit on ERROR
endlocal
exit /b 1
