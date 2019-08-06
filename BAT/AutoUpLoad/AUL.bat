@echo off

:start
if exist "123.txt" (
xcopy "123.txt" "\\bosch.com\dfsrb\DfsCN\DIV\CC\Tech\DA\11_DASy\00_Archive\Date_exchange\Marvin_HUANG\" /y
GOTO exit
) else (
sleep 2
echo ****************waiting****************
GOTO start
)

:exit
echo ***************************************
echo ***************finished****************
echo ***************************************
pause