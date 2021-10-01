//bool_cin.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// lesson 43: https://www.bilibili.com/video/BV1et411b73Z?p=43&spm_id_from=pageDriver
// 打印数组长度和首地址
int array_length () {
    int arr[10] = {1,2,3,4,5,6,7,8,9,10};
    cout << "length in RAM of the array: " << sizeof(arr) << endl;
    cout << "length in RAM of one item:  " << sizeof(arr[0]) << endl;
    cout << "length of the array:        " << sizeof(arr) / sizeof(arr[0]) << endl;

    cout << "starting address of array:  " << arr << endl;  // 直接写数组名即可显示数组首地址
    cout << "starting address of item 0: " << &arr[0] << endl;  // 显示数组元素首地址需要加 &
    
    // 将地址转换为十进制 int()
    cout << "starting address of item 0 in DEC: " << int(&arr[0]) << endl;
}

// 5只小猪比较体重
int sort_weight () {
    int arr[5] = {250, 350, 400, 750, 600};
    int max = 0;
    for (int i = 0; i < 5; i++) {
        max = (arr[i] > max ? arr[i] : max);
    }
    cout << "the max weight of 5 pigs: " << max << endl;
}

int main () {
    sort_weight();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}