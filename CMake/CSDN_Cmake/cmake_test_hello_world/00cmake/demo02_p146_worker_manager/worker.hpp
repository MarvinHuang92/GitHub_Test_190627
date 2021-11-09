// worker.hpp

#pragma once            // 防止头文件重复包含

#include <stdlib.h>
#include <iostream>
#include <string>

using namespace std;

// 职工抽象基类，包含普通员工，经理，老板
class Worker
{
public:
    // 显示个人信息
    virtual void showInfo() = 0;

    // 显示岗位名称
    virtual string getDeptName() = 0;

    int m_id;       // 工号
    string m_name;  // 姓名
    int m_deptId;   // 部门编号

};


