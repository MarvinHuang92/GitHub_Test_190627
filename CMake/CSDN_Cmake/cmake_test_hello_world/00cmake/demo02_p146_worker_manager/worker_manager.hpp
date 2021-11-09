// worker_manager.hpp

#pragma once            // 防止头文件重复包含

#include <stdlib.h>
#include <iostream>

using namespace std;

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

};


