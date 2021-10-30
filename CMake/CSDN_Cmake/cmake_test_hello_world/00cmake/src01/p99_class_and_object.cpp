// p99_class_and_object.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P99 类和对象

/* 面向对象三大特征：封装，继承，多态 */

// 定义一个圆类，求它的周长
const double PI = 3.1416;

class Circle 
{
public: // 访问权限
    // 成员 （包含“属性”和“方法”也叫“行为”）
    int m_r;  // 属性：半径
    
public:  // 属性和行为可以分开写，而且分别设置访问权限
    void set_radius(int r)  // 方法（行为）：允许用户设置半径
    {
        m_r = r;
    }
    double calculate_ZC ()  // 方法（行为）：计算周长 **注意这里不需要单独写形参
    {
        return 2*PI*m_r;
    }
};

void calculate_circle_ZC()
{
    // 创建对象实例
    Circle c1;
    c1.m_r = 10;  // 直接赋值
    c1.set_radius(10);  // 或者通过调用内部方法修改半径值
    cout << "圆的周长是： " << c1.calculate_ZC() << endl;  //  这里的calculate_ZC()后面不用分号
}

// P101 三种访问权限
/* 
1. public       类的内外都可以访问
2. protected    类内部可以访问，子类也可以访问
3. private      类内部可以访问，子类不可以访问

如果不写访问权限，则
struct 默认权限为 public
class  默认权限为 private
所以struct 和 class 没有太大的区别
*/

// private 属性的用法：
// 1. 对数据进行写保护：可读可写，只可读，只可写
//    将所有属性全都设置为 private ，再设置几个读写方法 (getName, setName)这种
//    如果禁止写，就不提供 setName 方法即可
// 2. 可以检查输入数据有效性，在 setName 中增加 if 格式或者范围的检查

// P104 立方体的相等判断
class Cube 
{
    private:
    int m_L, m_W, m_H;  // 长宽高

    public:
    // 设置长宽高
    void setL(int a)
    {
        m_L = a;
    }
    void setW(int a)
    {
        m_W = a;
    }
    void setH(int a)
    {
        m_H = a;
    }
    // 获取长宽高
    int getL()
    {
        return m_L;
    }
    int getW()
    {
        return m_W;
    }
    int getH()
    {
        return m_H;
    }

    
    int getS()  // 获取表面积
    {
        return 2*(m_L*m_W + m_W*m_H + m_L*m_H);
    }
    int getV()  // 获取体积
    {
        return m_L*m_W*m_H;
    }

    bool isSameByClass (Cube c2)  // 成员函数：判断和另一个立方体是否相等
    {
        if (m_L == c2.m_L && m_W == c2.m_W && m_H == c2.m_H)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
};

void Cube_instance ()
{
    Cube cb1;  // 创建立方体实例
    cb1.setL(2);
    cb1.setW(3);
    cb1.setH(4);
    cout << "S = " << cb1.getS() << endl;  // 计算表面积
    cout << "V = " << cb1.getV() << endl;  // 计算体积

    Cube cb2;  // 另一个立方体，用“成员函数”判断是否和第一个相等 （外部“全局函数”来判断就很简单，先不写了）
    cb2.setL(2);
    cb2.setW(3);
    cb2.setH(5);
    if (cb1.isSameByClass(cb2))
    {
        cout << "两个立方体是相等的" << endl;
    }
    else
    {
        cout << "两个立方体不相等" << endl;
    }
}




/*********************************************************************************************************/



int main_99 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    Cube_instance ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


