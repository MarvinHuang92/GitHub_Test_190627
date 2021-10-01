@echo off

@REM cmake install path:
set PATH="C:\TCC\Tools\cmake\3.12.1_WIN32\bin";%PATH%
set PATH="D:\Programming\Cmake\bin\bin";%PATH%

@REM compiler (g++, gcc) install path:
@REM set PATH="C:\TCC\Tools\selena_environment\0.1.7_WIN64\MSYS\mingw64\bin";%PATH%
set PATH="C:\TCC\Tools\mingw64\5.4.0_WIN64\bin";%PATH%
set PATH="D:\Programming\Cmake\MinGW\bin";%PATH%

echo Cleaning Old Build...
if exist build rd /S /Q build
mkdir build
sleep 2
pushd build

echo Running CMAKE...
echo.
@REM 可以用-D的形式直接定义缺少的参数，具体的值可以参考已有的项目编译结果中的 CmakeCache.txt
@REM 需要完整路径，而不是仅仅 mingw32-make.exe，否则会报错 compiler broken
set MAKE_EXE=D:/Programming/Cmake/MinGW/bin/mingw32-make.exe
if exist C:\TCC\Tools\mingw64\5.4.0_WIN64\bin set MAKE_EXE=C:/TCC/Tools/mingw64/5.4.0_WIN64/bin/mingw32-make.exe

@REM 需要增加 -G "MinGW Makefiles"参数，否则会默认调用 Visual Studio Generator 生成 sln 项目文件
call cmake.exe ../00cmake -G "MinGW Makefiles" -DCMAKE_MAKE_PROGRAM=%MAKE_EXE% 

@REM 完整的定义：
@REM set CXX_COMPILER=C:/TCC/Tools/selena_environment/0.1.7_WIN64/MSYS/mingw64/bin/g++.exe
@REM set C_COMPILER=C:/TCC/Tools/selena_environment/0.1.7_WIN64/MSYS/mingw64/bin/gcc.exe
@REM set GHS_CXX_COMPILER=C:/TCC/Tools/greenhills_ifx/comp_201815_4fp_WIN64/cxtri.exe
@REM set GHS_C_COMPILER=C:/TCC/Tools/greenhills_ifx/comp_201815_4fp_WIN64/cctri.exe

@REM call cmake.exe ../00cmake -G "MinGW Makefiles" -DCMAKE_CXX_COMPILER=%CXX_COMPILER% -DCMAKE_C_COMPILER=%C_COMPILER% -DCMAKE_AR=%GHS_CXX_COMPILER% 


echo.
echo Running MAKE...
echo.
call %MAKE_EXE% 


popd

pause
