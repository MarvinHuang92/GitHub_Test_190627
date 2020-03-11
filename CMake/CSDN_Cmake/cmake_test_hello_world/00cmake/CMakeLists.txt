#cmake最低版本需求，不加入此行会受到警告信息
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

#项目名称
PROJECT(HELLO)

#把当前目录(.)下所有源代码文件和头文件加入变量SRC_LIST
AUX_SOURCE_DIRECTORY(. SRC_LIST)

#生成应用程序 hello (在windows下会自动生成hello.exe)
ADD_EXECUTABLE(hello ${SRC_LIST})

#添加宏定义
ADD_DEFINITIONS(-DADD_DEFINITION)