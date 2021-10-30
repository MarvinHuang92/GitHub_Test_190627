// p105.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P105 - 判断点和圆的关系
/* 语言描述：
需要点类，和圆类（可以复用上面的，但需要增加一个属性，圆心）
圆心也是一个点（点类的一个实例）

需要几种方法：
点类: setX(int x) setY(int y)
圆类：setCenter(class Point &p) setRadius(int r)
     getDistance(&p1, &p2)
     isPointInCircle(center, radius)

注意这里的p用的是引用方式传递，可以节约一个内存地址
*/

// 包含所有类成员，注意只需要头文件（类声明），不需要包含相应的cpp文件（类成员函数实现）
#include "point.hpp"
#include "circle.hpp"


// 全局函数在这里定义
void circleCenter ()
{
    Point p;  // 创建点实例
    p.set_X(10);
    p.set_Y(0);
    cout << "点的坐标： " << p.get_X() << ", " << p.get_Y() << endl;

    Point center; //创建另一个点，作为圆心
    center.set_X(0);
    center.set_Y(0);
    cout << "圆心的坐标： " << center.get_X() << ", " << center.get_Y() << endl;

    Circle c1; // 创建圆实例
    c1.setCenter(center);
    c1.setRadius(10);

    double distance = c1.getDistance(p);
    cout << "两点的距离： " << distance << endl;

    if (distance < c1.getRadius())
    {
        cout << "点在圆内" << endl;
    }
    else if (distance > c1.getRadius())
    {
        cout << "点在圆外" << endl;
    }
    else
    {
        cout << "点在圆上" << endl;
    }
}


/*********************************************************************************************************/

int main_105 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    circleCenter ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}
