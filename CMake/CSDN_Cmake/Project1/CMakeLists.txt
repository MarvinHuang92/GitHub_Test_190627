cmake_minimum_required(VERSION 3.1)
# include(cmake/internal.cmake)
SET(CMAKE_C_COMPILER "gcc")
SET(CMAKE_CXX_COMPILER "g++")
#以上，指定编译器路径

#project name 指定生成的工程名为test_math
PROJECT(test_math)

#head file path 指定头文件目录为include
INCLUDE_DIRECTORIES(
include
)

#source directory 指定源文件目录为src，并将其赋值给环境变量DIR_SRCS
AUX_SOURCE_DIRECTORY(src DIR_SRCS)

#set environment variable 
#设定环境变量TEST_MATH的值为环境变量DIR_SRCS的值
#此处用于显示如何用环境变量对环境变量进行赋值
SET(TEST_MATH
${DIR_SRCS}
)

#set extern libraries
#将数学函数库赋值给环境变量LIBRARIES
#当然，可以不用这个环境变量，而在后面直接使用该库名
SET(LIBRARIES
libm.so
)

#add executable file
#用于指定生成文件，将环境变量TEST_MATH目录下的所有文件编译生成bin目录下的可执行文件bin
ADD_EXECUTABLE(run ${TEST_MATH})

#add link library
#指定bin/bin执行时的链接库为环境变量LIBRARIES的值－libm.so
#TARGET_LINK_LIBRARIES(run ${LIBRARIES})