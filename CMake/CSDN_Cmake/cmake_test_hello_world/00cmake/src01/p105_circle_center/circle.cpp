// circle.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// #include "circle.hpp"

// 所有类成员方法的实现  :: 之前的表示作用域（类名称）
// Circle类
void Circle::setCenter(Point &c)
{
    center = c;
}
void Circle::setRadius(int r)
{
    radius = r;
}
int Circle::getRadius()
{
    return radius;
}
double Circle::getDistance(Point &p)
{
    return sqrt(pow((p.get_X()-center.get_X()), 2) + pow((p.get_Y()-center.get_Y()), 2));
}


