// worker_manager.cpp

#include "worker_manager.hpp"
#include "worker.hpp"
#include "employee.hpp"
#include "manager.hpp"
#include "boss.hpp"

#include <fstream>
#define FILENAME "empFile.txt"

WorkerManager::WorkerManager()
{
    // // 初始化人数
    // this->m_EmpNum = 0;

    // // 初始化数组指针
    // this->m_EmpArray = NULL;

    // 读取存储的文件
    ifstream ifs;
    ifs.open(FILENAME, ios::in);

    // 文件不存在？
    if(! ifs.is_open())
    {
        cout << "档案文件不存在" << endl;
        this->m_EmpNum = 0;  // 初始化人数
        this->m_fileIsEmpty = true;  // 初始化文件为空的标志
        this->m_EmpArray = NULL;  // 初始化数组指针
        ifs.close();  // 关闭文件
        return;
    }
    else  // 文件存在
    {
        char ch;
        ifs >> ch;  // 右移一个字符
        if (ifs.eof())  // 如果右移之后读到 eof，说明文件为空
        {
            cout << "档案文件为空" << endl;
            this->m_EmpNum = 0;  // 初始化人数
            this->m_fileIsEmpty = true;  // 初始化文件为空的标志
            this->m_EmpArray = NULL;  // 初始化数组指针
            ifs.close();  // 关闭文件
            return;
        }
        else  // 文件不为空，读取文件中现有人数，并显示出来
        {
            int num = this->get_EmpNum();
            cout << "职工人数为： " << num << endl;
            this->m_EmpNum = num;  // 初始化人数

            this->m_fileIsEmpty = false;  // 初始化文件为空的标志
            this->m_EmpArray = new Worker*[this->m_EmpNum];  // 初始化数组指针：先创建堆区数组（开辟空间）
            this->init_Emp();   // 然后在数组中填充已知的数据

            // 显示测试用：
            for (int i = 0; i < this->m_EmpNum; i++)
            {
                cout << "第 " << i+1 << " 名职工： " 
                    << "编号：" << this->m_EmpArray[i]->m_id << " "
                    << "姓名：" << this->m_EmpArray[i]->m_name << " "
                    << "岗位：" << this->m_EmpArray[i]->m_deptId << endl;
            }

            ifs.close();  // 关闭文件
            return;
        }
    }
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
        
        // 更新标志：文件为不再为空
        this->m_fileIsEmpty = false;

        // 写入文件
        this->save();
    }
    else
    {
        cout << "输入有误。" << endl;
    }


    system("pause");
    system("cls");
}

void WorkerManager::save()
{
    ofstream ofs;
    ofs.open(FILENAME, ios::out);  // 写文件

    for(int i = 0; i < this->m_EmpNum; i++)
    {
        ofs << this->m_EmpArray[i]->m_id << " "
            << this->m_EmpArray[i]->m_name << " "
            << this->m_EmpArray[i]->m_deptId << endl;
    }
    
    ofs.close();
}

int WorkerManager::get_EmpNum()
{
    ifstream ifs;
    ifs.open(FILENAME, ios::in);

    int id;
    string name;
    int deptId;

    int num = 0;

    while (ifs >> id && ifs >> name && ifs >> deptId)
    {
        // 记录人数
        num++;
    }
    ifs.close();

    return num;
}

void WorkerManager::init_Emp()
{
    ifstream ifs;
    ifs.open(FILENAME, ios::in);

    int id;
    string name;
    int deptId;

    int index = 0;  // 数组脚标

    while (ifs >> id && ifs >> name && ifs >> deptId)
    {
        // 创建具体的职工
        Worker * worker = NULL;
        if (deptId == 1)  // 普通职工
        {
            worker = new Employee(id, name, deptId);
        }
        else if (deptId == 2)  // 经理
        {
            worker = new Manager(id, name, deptId);
        }
        else if (deptId == 3)  // 老板
        {
            worker = new Boss(id, name, deptId);
        }

        this->m_EmpArray[index] = worker;
        index++;
    }
    ifs.close();
}