#cmake最低版本需求，不加入此行会受到警告信息
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

#指定编译器路径

# SET(CMAKE_TOOLCHAIN_FILE CMakeTst.cmake)
# SET(CMAKE_GENERATOR "Unix Makefiles")

# INCLUDE(CMakeForceCompiler)
SET(CMAKE_SYSTEM_NAME Windows)
# SET(CMAKE_C_COMPILER_FORCED TRUE)
# CMAKE_FORCE_C_COMPILER(gcc GNU) 
# CMAKE_FORCE_CXX_COMPILER(g++ GNU) 

set(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "")
set(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS "")

#项目名称
PROJECT(HELLO)
SET(CMAKE_EXECUTABLE_SUFFIX .exe)

#把当前目录(.)下所有源代码文件和头文件加入变量SRC_LIST，不含子目录
# AUX_SOURCE_DIRECTORY(. SRC_LIST)
# AUX_SOURCE_DIRECTORY(src00 SRC_LIST)
# AUX_SOURCE_DIRECTORY(src01 SRC_LIST)
# AUX_SOURCE_DIRECTORY(src02 SRC_LIST)
# AUX_SOURCE_DIRECTORY(demo02_p146_worker_manager SRC_LIST)
AUX_SOURCE_DIRECTORY(src03 SRC_LIST)

#如果有子目录，需要设置不同的名字，并在 ADD_EXECUTABLE 中加入相应的名字
# AUX_SOURCE_DIRECTORY(src01/p105_circle_center SRC_LIST_105)

#设置文件编码
    # for MSVS compiler
    # add_compile_options("$<$<C_COMPILER_ID:MSVC>:/source-charset:utf-8>")
    # add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/source-charset:utf-8>")

    # for GCC
    add_compile_options("-fexec-charset=GBK")       # 源代码字符集：GBK
    add_compile_options("-finput-charset=UTF-8")    # 目标显示字符集：UTF-8

#生成应用程序 hello (在windows下会自动生成hello.exe)
# ADD_EXECUTABLE(hello ${SRC_LIST} ${SRC_LIST_105})
ADD_EXECUTABLE(hello ${SRC_LIST})

#添加宏定义
ADD_DEFINITIONS(-DADD_DEFINITION)

#添加此定义，防止出现 “找不到libstdc++-6.dll,无法继续执行代码.” 的报错
set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++")

