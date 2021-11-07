// p141_polymorphic_2.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;


// P141 - 实例：组装一些电脑
// 各种零件的抽象类
class AbstractCPU
{
public:
    // 抽象计算函数
    virtual void calculate() = 0;
};
class AbstractGPU
{
public:
    // 抽象显示函数
    virtual void display() = 0;
};
class AbstractMemory
{
public:
    // 抽象存储函数
    virtual void storage() = 0;
};

// 各种零件的实体类
class IntelCPU : public AbstractCPU
{
    // 重写父类的虚函数
    void calculate()
    {
        cout << "Intel CPU 正在进行 Calculate 工作" << endl;
    }
};
class AmdCPU : public AbstractCPU
{
    // 重写父类的虚函数
    void calculate()
    {
        cout << "AMD CPU 正在进行 Calculate 工作" << endl;
    }
};
class IntelGPU : public AbstractGPU
{
    // 重写父类的虚函数
    void display()
    {
        cout << "Intel GPU 正在进行 Display 工作" << endl;
    }
};
class AmdGPU : public AbstractGPU
{
    // 重写父类的虚函数
    void display()
    {
        cout << "AMD GPU 正在进行 Display 工作" << endl;
    }
};
class KingstonMemory : public AbstractMemory
{
    // 重写父类的虚函数
    void storage()
    {
        cout << "Kingston Memory 正在进行 Storage 工作" << endl;
    }
};
class SamsungMemory : public AbstractMemory
{
    // 重写父类的虚函数
    void storage()
    {
        cout << "Samsung Memory 正在进行 Storage 工作" << endl;
    }
};

class Computer
{
public:
    // 构造函数中传入三个零件的指针 （不能传值，只能是指针或者引用，否则报错抽象类无法实例化对象）
    Computer(AbstractCPU * cpu, AbstractGPU * gpu, AbstractMemory * memory)
    {
        m_cpu = cpu;
        m_gpu = gpu;
        m_memory = memory;
    }

    // 让电脑工作的函数
    void work()
    {
        m_cpu->calculate();
        m_gpu->display();
        m_memory->storage();
    }

    // 析构函数：释放各个零件的堆区内存
    ~Computer()
    {
        if (m_cpu != NULL)
        {
            delete m_cpu;
            m_cpu = NULL;
        }
        if (m_gpu != NULL)
        {
            delete m_gpu;
            m_gpu = NULL;
        }
        if (m_memory != NULL)
        {
            delete m_memory;
            m_memory = NULL;
        }
    }

private:
    AbstractCPU * m_cpu;
    AbstractGPU * m_gpu;
    AbstractMemory * m_memory;
};



void test_141_00()
{
    // 创建各种零件(可以具体区分到 intelCpu_1,2... 这里偷懒了，假装每个零件可以同时装在不同的电脑上吧)
    // 还可以更懒，直接在创建computer时候在参数中 new
    // AbstractCPU * intelCpu = new IntelCPU;
    // AbstractGPU * intelGpu = new IntelGPU;
    // AbstractMemory * kingstonMemory = new KingstonMemory;

    // AbstractCPU * amdCpu = new AmdCPU;
    // AbstractGPU * amdGpu = new AmdGPU;
    // AbstractMemory * samsungMemory = new SamsungMemory;

    // 组装不同的电脑
    cout << "第一台电脑开机..." << endl;
    Computer * computer_1 = new Computer(new IntelCPU, new IntelGPU, new KingstonMemory);
    computer_1->work();
    delete computer_1;
    computer_1 = NULL;

    cout << "第二台电脑开机..." << endl;
    Computer * computer_2 = new Computer(new AmdCPU, new AmdGPU, new SamsungMemory);
    computer_2->work();
    delete computer_2;
    computer_2 = NULL;

    cout << "第三台电脑开机..." << endl;
    Computer * computer_3 = new Computer(new IntelCPU, new AmdGPU, new KingstonMemory);
    computer_3->work();
    delete computer_3;
    computer_3 = NULL;

    // 注意这里只释放了 computer，各个零件的释放，在computer类的析构函数中实现。
}

/*********************************************************************************************************/



int main_141 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_141_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


