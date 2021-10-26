// p84_memory_management.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P84 - 程序内存管理
void Hello2 () 
{
    // Dummy Function
    cout << "Hello World Again." << endl;
}



// 是否需要显示中文？
bool ChineseDisplay = false;

int main () {
    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")

    Hello2 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


