//s03_two_dimension_array_lesson_47.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// lesson 47: https://www.bilibili.com/video/BV1et411b73Z?p=43&spm_id_from=pageDriver
// 定义二维数组
int def_2d_array ()
{
    int arr[2][3] = 
    {
        {250, 350, 400}, 
        {750, 600, 900}
    };
    int length_row = sizeof(arr) / sizeof (arr[0]);  // 计算数组长度_行数
    int length_col = sizeof(arr[0]) / sizeof (arr[0][0]);  // 计算数组长度_列数
    
    // 打印数组
    cout << "original array:" << endl;
    for (int i=0; i<length_row; i++) {
        for (int j=0; j<length_col; j++) {
            cout << arr[i][j] << " ";  // 每一行内不换行，只显示空格
        }
        cout << endl;   // 一行结束后再换行
    }

    // 打印地址
    cout << "length in RAM of the 2d array:     " << sizeof(arr) << endl;
    cout << "length in RAM of a row in array:   " << sizeof(arr[0]) << endl;
    cout << "number of rows of the array:       " << sizeof(arr) / sizeof(arr[0]) << endl;
    cout << "number of cols of the array:       " << sizeof(arr[0]) / sizeof(arr[0][0]) << endl;

    cout << "starting address of 2d array:      " << arr << endl;  // 直接写数组名即可显示数组首地址
    cout << "starting address of first row:     " << arr[0] << endl;
    cout << "starting address of first item:    " << &arr[0][0] << endl;  // 显示数组元素首地址需要加 &
    
    // 使用long long类型，防止地址长度作为int溢出
    cout << "starting address of item 0 in DEC: " << (long long)&arr[0][0] << endl;
}

int main3 () {
    def_2d_array();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}





/*
看到了指针：P56
https://www.bilibili.com/video/BV1et411b73Z?p=56&spm_id_from=pageDriver

2021.10.9

P55 也可以再看一下，头文件和源文件的格式范例，当然以后想起来再看亦可以
*/
