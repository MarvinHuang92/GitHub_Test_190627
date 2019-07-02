cmake_minimum_required(VERSION 3.1)
# include(cmake/internal.cmake)
SET(CMAKE_C_COMPILER "gcc")
SET(CMAKE_CXX_COMPILER "g++")
#以上，指定编译器路径

PROJECT (HELLO)
SET(SRC_LIST main.cpp)
MESSAGE(STATUS "This is BINARY dir " ${HELLO_BINARY_DIR})
MESSAGE(STATUS "This is SOURCE dir "${HELLO_SOURCE_DIR})
ADD_EXECUTABLE(hello ${SRC_LIST})