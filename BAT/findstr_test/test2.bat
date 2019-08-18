@echo off

:: there should be a space between "if syntax" and (
:: similarly for else

if "%~1"=="" (
echo no attributes
) else (
echo %0 %1
)

pause