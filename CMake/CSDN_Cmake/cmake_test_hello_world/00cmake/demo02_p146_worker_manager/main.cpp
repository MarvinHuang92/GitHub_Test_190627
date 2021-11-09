// main.cpp

#include "worker_manager.hpp"

int main()
{
    // 显示中文
    system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    // Do Something
    WorkerManager wm;
    int choice = 0;
    while(true)
    {
        // 展示菜单
        wm.showMenu();
        cout << "请输入选择： " << endl;
        cin >> choice;

        switch(choice)
        {
        case 0:  // 退出系统
            wm.exitSystem();
            break;
        case 1:  // 添加职工
            break;
        case 2:  // 显示职工
            break;
        case 3:  // 删除职工
            break;
        case 4:  // 修改职工
            break;
        case 5:  // 查找职工
            break;
        case 6:  // 按照工号排序
            break;
        case 7:  // 清空文件
            break;
        default: // 如果输入格式错误，直接清空屏幕再次循环 while (true)
            system("cls");
            break;
        }
    }
    



    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}