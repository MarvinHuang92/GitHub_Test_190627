// manager.hpp

#pragma once            // 防止头文件重复包含

#include <stdlib.h>
#include <iostream>
#include <string>

#include "worker.hpp"

using namespace std;

// 普通员工类
class Manager: public Worker
{
public:
    // 构造函数
    Manager(int id, string name, int deptId);

    // 显示个人信息
    virtual void showInfo();

    // 显示岗位名称
    virtual string getDeptName();

};


