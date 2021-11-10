// worker_manager.cpp

#include "worker_manager.hpp"
#include "worker.hpp"
#include "employee.hpp"
#include "manager.hpp"
#include "boss.hpp"

WorkerManager::WorkerManager()
{
    // 初始化人数
    this->m_EmpNum = 0;

    // 初始化数组指针
    this->m_EmpArray = NULL;
}

WorkerManager::~WorkerManager()
{

}

void WorkerManager::showMenu()
{
    cout << "****************************" << endl;
    cout << "*** 欢迎使用职工管理系统 ***" << endl;
    cout << "*** 0.  退出管理系统 *******" << endl;
    cout << "*** 1.  添加职工信息 *******" << endl;
    cout << "*** 2.  显示职工信息 *******" << endl;
    cout << "*** 3.  删除离职职工 *******" << endl;
    cout << "*** 4.  修改职工信息 *******" << endl;
    cout << "*** 5.  查找职工信息 *******" << endl;
    cout << "*** 6.  按照工号排序 *******" << endl;
    cout << "*** 7.  清空所有文档 *******" << endl;
    cout << "****************************" << endl;
    cout << endl;

}

void WorkerManager::exitSystem()
{
    cout << "欢迎下次使用！" << endl;
    system("pause");
    exit(0);
}

void WorkerManager::Add_Emp()
{
    cout << "需要添加多少位员工？" << endl;

    int addNum = 0;
    cin >> addNum;

    if (addNum > 0)
    {
        // 计算新的空间大小
        int newSize = this->m_EmpNum + addNum;

        // 开辟新空间
        Worker ** newSpace = new Worker*[newSize];

        // 将原空间的内容放到新空间
        if (this->m_EmpArray != NULL)
        {
            for (int i = 0; i < this->m_EmpNum; i++)
            {
                newSpace[i] = this->m_EmpArray[i];
            }
        }

        // 输入新数据
        for (int i = 0; i < addNum; i++)
        {
            int id;
            string name;
            int dSelect;

            cout << "请输入第 " << i+1 << " 个新职工编号： " << endl;
            cin >> id;

            cout << "请输入第 " << i+1 << " 个新职工姓名： " << endl;
            cin >> name;

            cout << "请选择该职工的岗位：" << endl;
            cout << "1. 普通职工" << endl;
            cout << "2. 经理" << endl;
            cout << "3. 老板" << endl;
            cin >> dSelect;

            Worker * worker = NULL;  // 注意这里 worker 的类型是 Worker*，是一个指针
            switch(dSelect)
            {
            case 1:  // 普通职工
                worker = new Employee(id, name, 1);
                break;
            case 2:  // 经理
                worker = new Manager(id, name, 2);
                break;
            case 3:  // 老板
                worker = new Boss(id, name, 3);
                break;
            default:
                break;
            }

            newSpace[this->m_EmpNum + i] = worker;  // 这个数组里面存储的全是指针（Employee或者Manager或者Boss类对象的地址）
                                                    // 所以构成了多态，Worker * 指向 Employee或者Manager或者Boss类对象
        }

        // 释放原有空间
        delete[] this->m_EmpArray;

        // 更改新空间的指向
        this->m_EmpArray = newSpace;

        // 更新当前人数
        this->m_EmpNum = newSize;

        // 提示添加成功
        cout << "成功添加了 " << addNum << " 名新职工。" << endl;
    }
    else
    {
        cout << "输入有误。" << endl;
    }


    system("pause");
    system("cls");
}