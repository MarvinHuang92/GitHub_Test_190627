// point.hpp

// 防止头文件重复包含，只需要写在hpp中，不需要写在cpp中
#pragma once

using namespace std;

// P105 - 判断点和圆的关系

// 在头文件中仅仅声明成员属性和方法，不需要方法的实现
class Point 
{
    private:
    int pos_X;
    int pos_Y;

    public:
    int get_X ();
    int get_Y ();
    void set_X (int a);
    void set_Y (int a);
};

