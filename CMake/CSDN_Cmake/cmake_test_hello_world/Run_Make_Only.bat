@echo off

@REM cmake install path:
set PATH="C:\TCC\Tools\cmake\3.12.1_WIN32\bin";%PATH%
set PATH="D:\Programming\Cmake\bin\bin";%PATH%

@REM compiler (g++, gcc) install path:
@REM set PATH="C:\TCC\Tools\selena_environment\0.1.7_WIN64\MSYS\mingw64\bin";%PATH%
set PATH="C:\TCC\Tools\mingw64\5.4.0_WIN64\bin";%PATH%
set PATH="D:\Programming\Cmake\MinGW\bin";%PATH%

pushd build

@REM 需要完整路径，而不是仅仅 mingw32-make.exe，否则会报错 compiler broken
set MAKE_EXE=D:/Programming/Cmake/MinGW/bin/mingw32-make.exe
if exist C:\TCC\Tools\mingw64\5.4.0_WIN64\bin set MAKE_EXE=C:/TCC/Tools/mingw64/5.4.0_WIN64/bin/mingw32-make.exe

echo.
echo Running MAKE...
echo.
call %MAKE_EXE% 


popd

pause
