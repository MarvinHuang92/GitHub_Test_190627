REM ########## Dont use space when set attribute as ="%1" ="%2" ##############

@echo off
title Create_A_Zipfile
setlocal

set TargetFileName=%1
set ResourceFolder=%2
REM the first attribute is name of target zip file
REM the second attribute is the folder you want to put into the zip file

set ZIP_EXECUTABLE="C:\Program Files\7-Zip\7z.exe"

call %ZIP_EXECUTABLE% a -r -tzip %TargetFileName% %ResourceFolder%

endlocal
exit /b 0