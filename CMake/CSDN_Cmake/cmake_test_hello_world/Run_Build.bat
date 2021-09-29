@echo off

set PATH="C:\TCC\Tools\cmake\3.12.1_WIN32\bin";%PATH%
@REM set PATH="C:\TCC\Tools\selena_environment\0.1.7_WIN64\MSYS\mingw64\bin";%PATH%
set PATH="C:\TCC\Tools\mingw64\5.4.0_WIN64\bin";%PATH%

echo Cleaning Old Build...
if exist build rd /S /Q build
mkdir build
sleep 2
pushd build

echo Running CMAKE...
echo.
@REM 可以用-D的形式直接定义缺少的参数，具体的值可以参考已有的项目编译结果中的 CmakeCache.txt
set MAKE_EXE=C:/TCC/Tools/mingw64/5.4.0_WIN64/bin/mingw32-make.exe

set CXX_COMPILER=C:/TCC/Tools/selena_environment/0.1.7_WIN64/MSYS/mingw64/bin/g++.exe
set C_COMPILER=C:/TCC/Tools/selena_environment/0.1.7_WIN64/MSYS/mingw64/bin/gcc.exe

set GHS_CXX_COMPILER=C:/TCC/Tools/greenhills_ifx/comp_201815_4fp_WIN64/cxtri.exe
set GHS_C_COMPILER=C:/TCC/Tools/greenhills_ifx/comp_201815_4fp_WIN64/cctri.exe

call cmake.exe ../00cmake -G "MinGW Makefiles" -DCMAKE_MAKE_PROGRAM=%MAKE_EXE% 
@REM call cmake.exe ../00cmake -DCMAKE_MAKE_PROGRAM=%MAKE_EXE% 
REM call cmake.exe ../00cmake
REM call cmake.exe ../00cmake -G "NMake Makefiles" -DCMAKE_CXX_COMPILER=%CXX_COMPILER% -DCMAKE_C_COMPILER=%C_COMPILER%
@REM  -DCMAKE_AR=%GHS_CXX_COMPILER% 

@REM -G "Unix Makefiles"

echo.
echo Running MAKE...
echo.
call %MAKE_EXE% 


popd

pause
