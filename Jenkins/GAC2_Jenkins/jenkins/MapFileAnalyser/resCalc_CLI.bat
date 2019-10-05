@echo off 


REM #	Parameters:				Description:
REM #	%1: Variant String 		This String is necessary to declare if a DASyBase or DASyENH Software build is active. Following options are possible:
REM			bjev_my20_base 		(for DASy Base)
REM			bjev_my20_enh 		(for DASy Enhance)

echo ************************************************************

echo resCalc_CLI
echo Project must be compiled first -> *.map file must exsist

echo ************************************************************

if "%1" == "" (
echo "no Variant Code as Parameter 1 (bjev_my20_base or bjev_my20_enh) available"

exit 1 )

set VARIANT_CODE=%1
REM get drive, path of root_parent
for %%A in ("%~dp0\..\..") do set "root_parent=%%~fA"
echo root_parent: %root_parent%
echo.
SET mapName=%root_parent%\generatedFiles\%VARIANT_CODE%\exec\%VARIANT_CODE%.map
echo mapName: %mapName%
echo.

if not exist %mapName% (
	echo Error: File %mapName% missing
 	
	exit -1
)

SET layout=%root_parent%\jenkins\MapFileAnalyser\memory_layout.xml
echo layout: %layout%
echo.
SET ghsPath=C:\TCC\Tools\greenhills_ifx\comp_201715_1fp_WIN\decode.exe
echo ghsPath: %ghsPath%
echo.
SET reportPath=%root_parent%\generatedFiles\%VARIANT_CODE%
echo reportPath: %reportPath%
echo.
SET resCalcPath=ghs_map_resourcecalculator_release
echo resCalcPath: %resCalcPath%
echo.

SET reportXML=%reportPath%\%VARIANT_CODE%_report.xml
REM clean old output
if exist %reportXML% (
del %reportXML% )

echo ***************************
echo Calling resCalcAurixCLI.exe 
echo ***************************
cd %root_parent%\jenkins\MapFileAnalyser\%resCalcPath%

call resCalcAurixCLI.exe -mapName="%mapName%" -layout="%layout%" -ghsPath="%ghsPath%" -reportPath="%reportPath%"
echo.
if exist %reportXML% (
	echo OK: report.xml generated -see: %reportXML%
	
	exit /b 0
) else (
	echo Error: report.xml generation failed
	
	exit -1
)