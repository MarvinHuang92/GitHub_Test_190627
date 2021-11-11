// worker_manager.hpp

#pragma once            // 防止头文件重复包含

#include <stdlib.h>
#include <iostream>

using namespace std;

#include "worker.hpp"

// P149 - 管理类：用户菜单界面 + 增删改查操作 + 文件管理
class WorkerManager
{
public:
    // 构造函数声明
    WorkerManager();
    
    // 展示菜单
    void showMenu();

    // 退出系统
    void exitSystem();

    // 析构函数声明
    ~WorkerManager();

    // 文件中的人数
    int m_EmpNum;

    // 员工数组指针
    Worker ** m_EmpArray;

    // 增加职工的函数
    void Add_Emp();

    // 保存文件
    void save();

    // 标志文件是否为空
    bool m_fileIsEmpty;

    // 从文件中读取人数
    int get_EmpNum();

    // 初始化员工
    void init_Emp();

};


