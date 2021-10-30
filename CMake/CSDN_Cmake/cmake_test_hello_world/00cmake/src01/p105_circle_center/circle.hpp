// circle.hpp

// 防止头文件重复包含，只需要写在hpp中，不需要写在cpp中
#pragma once

using namespace std;

// P105 - 判断点和圆的关系

const double PI = 3.1416;

#include "point.hpp"

// 在头文件中仅仅声明成员属性和方法，不需要方法的实现
class Circle
{
    private:
    int radius;
    Point center;  // 类成员属性，可以是另一个类成员

    public:
    // 每一个属性都可以对应一个get和set方法，但这里圆心只需要set不需要get
    void setCenter(Point &c);
    void setRadius(int r);
    int getRadius();

    // 获取一个点到圆心的距离
    double getDistance(Point &p);
};

