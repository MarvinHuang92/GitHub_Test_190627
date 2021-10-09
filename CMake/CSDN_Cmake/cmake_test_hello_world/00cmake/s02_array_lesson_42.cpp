//s02_array_lesson_42.cpp

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
    // cout << "starting address of item 0 in DEC: " << int(&arr[0]) << endl;

    // 使用long long类型，防止地址长度作为int溢出
    cout << "starting address of item 0 in DEC: " << (long long)&arr[0] << endl;
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

// 数组元素逆置
int array_revert () {
    int arr[5] = {250, 350, 400, 750, 600};
    int length = sizeof(arr) / sizeof (arr[0]);  // 计算数组长度
    
    // 打印初始数组
    cout << "original array:" << endl;
    for (int i=0; i<length; i++) {
        cout << arr[i] << endl;
    }

    int start_index = 0;  // 起始元素下标
    int end_index = length - 1;  // 末尾元素下标
    int temp = 0;  // 临时元素值存储

    // 互换首尾元素值
    while (start_index < end_index)
    {
        temp = arr[start_index];
        arr[start_index] = arr[end_index];
        arr[end_index] = temp;
        
        start_index ++;  // 修改首尾下标值
        end_index --;
    }
    
    // 打印逆置后的数组
    cout << "finished array:" << endl;
    for (int i=0; i<length; i++) {
        cout << arr[i] << endl;
    }
}

// 冒泡排序：升序
int bubble_sort () {
    int arr[10] = {250, 350, 400, 750, 600, 900, 120, 95, 0, 520};
    int length = sizeof(arr) / sizeof (arr[0]);  // 计算数组长度
    
    // 打印初始数组
    cout << "original array:" << endl;
    for (int i=0; i<length; i++) {
        cout << arr[i] << endl;
    }

    int start_index = 0;  // 起始元素下标
    int end_index = length - 1;  // 末尾元素下标
    int temp = 0;  // 临时元素值存储

    // 开始排序
    while (end_index > start_index)  // 外层循环：起始下标不变，结尾下标每次减1
    {
        for (int i=start_index; i<end_index; i++)  // 内层循环：每一轮排序中，如果相邻两个值，前者大于后者，则互换它们
        {
            if (arr[i] > arr[i+1])
            {
                temp = arr[i];
                arr[i] = arr[i+1];
                arr[i+1] = temp;
            }
        }
        end_index --;  // 修改末尾下标值，然后进入下一轮排序 （每一轮比较的次数比上一轮少一次）
    }
    
    // 打印逆置后的数组
    cout << "finished array:" << endl;
    for (int i=0; i<length; i++) {
        cout << arr[i] << endl;
    }
}

int main2 () {
    bubble_sort();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}