//s01_bool_cin.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// bool类型不支持输入字符串 true / false，只接受数字输入
int bool_cin() {
    bool flag = false;
    cout << "Please input a bool value:" << endl;
    cin >> flag;
    cout << "Flag = " << flag << endl;
}

// 猜数字游戏
int guess_number () {
    // 利用系统时间生成随机数，否则这个rand()随机数在编译的时候就固定了，重复执行exe不会改变随机数
    srand((unsigned int) time(NULL));

    // 随机生成一个1-100的数字 （由0-99的随机数 +1 得到）
    int num = rand() % 100 + 1;
    int input_num = 0;

    // cout << "The Random number is " << num << endl;

    while(1) {
        cout << "Please input a number:" << endl;
        cin >> input_num;
        // cout << "Your input is " << input_num << endl;

        if (input_num == num)
        {
            cout << "You guess correct!" << endl;
            break;
        }
        else if (input_num < num)
        {
            cout << "Your input is too small!" << endl;
        }
        else // if (input_num > num)
        {
            cout << "Your input is too large!" << endl;
        }
        cout << endl;  // leave an empty line.
    }
}

// 求所有三位数中的水仙花数（各个位数的三次幂之和等于数字本身）
int narcissu_num () {
    // int num = 0;  //可以直接在for里面定义变量
    int a, b, c;
    for (int num = 100; num < 1000; num++) {
        // cout << num << endl;
        a = num / 100;
        b = (num % 100 ) / 10;
        c = num % 10;
        // cout << a << b << c << endl;
        if (pow(a, 3) + pow(b, 3) + pow(c, 3) == num) {
            cout << num << endl;
        }
    }
}

// 不能说7 (从1到100)
int dont_count_7 () {
    // int num = 0;  //可以直接在for里面定义变量
    int a, b, c;
    for (int num = 1; num <= 100; num++) {
        // cout << num << endl;
        a = num / 100;
        b = (num % 100 ) / 10;
        c = num % 10;
        // cout << a << b << c << endl;
        if (a == 7 || b == 7 || c== 7 || num % 7 == 0) {
            cout << "XXX" << endl;
        }
        else
        {
            cout << num << endl;
        }
    }
}

// 打印乘法口诀表
int multiply_table () {
    for (int i = 1; i < 10; i++) {
        for (int j = 1; j <= i; j++) {
            cout << j << "*" << i << "=" << i*j << "\t";
        }
        cout << endl;
    }
}


int main1 () {
    multiply_table();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}