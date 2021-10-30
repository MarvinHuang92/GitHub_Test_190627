// point.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// #include "point.hpp"

// 所有类成员方法的实现  :: 之前的表示作用域（类名称）
// Point类
int Point::get_X ()
{
    return pos_X;
}
int Point::get_Y ()
{
    return pos_Y;
}
void Point::set_X (int a)
{
    pos_X = a;
}
void Point::set_Y (int a)
{
    pos_Y = a;
}
