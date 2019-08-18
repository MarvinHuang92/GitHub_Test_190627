::@echo off

@cd "C:\Local_Disk\GitHub_Test_190627\BAT\findstr_test"

findstr /l "12345" abc.txt
if %ERRORLEVEL% ==1 GOTO nothing_found
else GOTO found

:found
echo "found"
GOTO EXIT

:nothing_found
echo "nothing found!"
GOTO EXIT

:EXIT
pause