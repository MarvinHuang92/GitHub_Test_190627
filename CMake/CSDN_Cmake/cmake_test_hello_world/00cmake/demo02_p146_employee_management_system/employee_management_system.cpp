// employee_management_system.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

#include <fstream> // 用于文件操作

// P143 - 文件操作：写文件



/*********************************************************************************************************/



int main () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_146_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


