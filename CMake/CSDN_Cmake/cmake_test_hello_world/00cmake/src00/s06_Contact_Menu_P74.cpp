//s06_AdressBook_Menu_P74.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P74 - 开始制作联系人系统
void showMenu () 
{
    // 只是单纯的显示菜单上的文字
    cout << "*********************" << endl;
    cout << "*** 1. 新建联系人 ***" << endl;
    cout << "*** 2. 显示联系人 ***" << endl;
    cout << "*** 3. 删除联系人 ***" << endl;
    cout << "*** 4. 查找联系人 ***" << endl;
    cout << "*** 5. 修改联系人 ***" << endl;
    cout << "*** 6. 清空通信录 ***" << endl;
    cout << "*** 0. 退出通信录 ***" << endl;
    cout << "*********************" << endl;
}

// 联系人结构体
struct Person {
    string name;
    int sex;   // 1-男， 2-女
    int age;
    string phonenumber;
    string address;
};

// 通讯录结构体
#define MAX 2 // 人数上限
struct AdressBook {
    struct Person personArray[MAX];
    // int Size = 0;  // 现有人数，直接在这里初始化会有warning，建议在实例创建时再初始化
    int Size;
};

// 函数1：新建联系人，利用地址传递可以直接修改实参
void addPerson(AdressBook * Abs)
{
    // 首先判断是否已满
    if (Abs->Size < MAX)  // 注意这里是<而不是<=
    {
        cout << "请输入姓名： " << endl;
        cin >> Abs->personArray[Abs->Size].name;
        
        cout << "请输入性别(1-男 2-女)： " << endl;
        int sex = 0;
        // 检查输入合法性
        while (true)
        {
            cin >> sex;
            if (sex == 1 || sex == 2)
            {
                Abs->personArray[Abs->Size].sex = sex;
                break;
            }
            cout << "输入格式不正确！" << endl;
        }
        
        cout << "请输入年龄： " << endl;
        cin >> Abs->personArray[Abs->Size].age;
        cout << "请输入电话号码： " << endl;
        cin >> Abs->personArray[Abs->Size].phonenumber;
        cout << "请输入地址： " << endl;
        cin >> Abs->personArray[Abs->Size].address;

        Abs->Size ++;

        cout << "添加成功！" << endl;
    } 
    else 
    {
        cout << "通讯录已满！" << endl;
    }
    system("pause");
    system("cls");  // 清屏
}

// 函数2：显示所有联系人
void showPerson(AdressBook * Abs)
{
    // 首先判断通讯录是否为空
    if (Abs->Size > 0)
    {
        for (int i=0; i<Abs->Size; i++)
        {
            string sex = "男";
            if (Abs->personArray[i].sex == 2) sex = "女";

            cout << "姓名:\t" << Abs->personArray[i].name 
                << "\t性别:\t" << sex // 也可以用三目运算符 (Abs->personArray[i].sex == 1? "男" : "女")
                << "\t年龄:\t" << Abs->personArray[i].age 
                << "\t电话号码:\t" << Abs->personArray[i].phonenumber 
                << "\t地址:\t" << Abs->personArray[i].address 
                << endl;
        }
    } 
    else 
    {
        cout << "通讯录为空！" << endl;
    }
    system("pause");
    system("cls");  // 清屏
}

// 函数3.1：检查联系人是否存在，如果存在返回他在数组中的下标，如果不存在返回-1
int isExist(AdressBook * Abs, string person_name)
{
    for (int i=0; i<Abs->Size; i++)
    {
        if (Abs->personArray[i].name == person_name) return i;
    }
    return -1;
}

// 函数3.2：删除指定的联系人
void removePerson(AdressBook * Abs)
{
    string person_name;
    cout << "请输入联系人姓名：" << endl;
    cin >> person_name;

    // 首先判断联系人是否存在
    int ret = isExist(Abs, person_name);
    if (ret == -1)  // 内部调用另一个函数时，不需要再次使用传址符号 &，Abs本身就是地址
    {
        cout << "查无此人！" << endl;
    }
    else
    {
        // 删除的逻辑：将所有后面的数据依次前移一位，并让size --
        cout << "找到此人。" << endl;
        for (int i=ret; i<Abs->Size-1; i++) // 注意这里Size要减1，不然最后一个元素会越界
        {
            Abs->personArray[i] = Abs->personArray[i+1];
        }
        Abs->Size --;
        cout << "删除成功。" << endl;
    }
    system("pause");
    system("cls");  // 清屏
}

// 函数4：查找指定的联系人
void searchPerson(AdressBook * Abs)
{
    string person_name;
    cout << "请输入联系人姓名：" << endl;
    cin >> person_name;

    // 首先判断联系人是否存在
    int ret = isExist(Abs, person_name);
    if (ret == -1)  // 内部调用另一个函数时，不需要再次使用传址符号 &，Abs本身就是地址
    {
        cout << "查无此人！" << endl;
    }
    else
    {
        cout << "找到此人。" << endl;
        string sex = "男";
        if (Abs->personArray[ret].sex == 2) sex = "女";

        cout << "姓名:\t" << Abs->personArray[ret].name 
            << "\t性别:\t" << sex // 也可以用三目运算符 (Abs->personArray[ret].sex == 1? "男" : "女")
            << "\t年龄:\t" << Abs->personArray[ret].age 
            << "\t电话号码:\t" << Abs->personArray[ret].phonenumber 
            << "\t地址:\t" << Abs->personArray[ret].address 
            << endl;
    }
    system("pause");
    system("cls");  // 清屏
}

// 函数5：修改指定的联系人
void editPerson(AdressBook * Abs)
{
    string person_name;
    cout << "请输入联系人姓名：" << endl;
    cin >> person_name;

    // 首先判断联系人是否存在
    int ret = isExist(Abs, person_name);
    if (ret == -1)  // 内部调用另一个函数时，不需要再次使用传址符号 &，Abs本身就是地址
    {
        cout << "查无此人！" << endl;
    }
    else
    {
        cout << "找到此人。修改信息中..." << endl;

        cout << "请输入姓名： " << endl;
        cin >> Abs->personArray[ret].name;
        
        cout << "请输入性别(1-男 2-女)： " << endl;
        int sex = 0;
        // 检查输入合法性
        while (true)
        {
            cin >> sex;
            if (sex == 1 || sex == 2)
            {
                Abs->personArray[ret].sex = sex;
                break;
            }
            cout << "输入格式不正确！" << endl;
        }
        
        cout << "请输入年龄： " << endl;
        cin >> Abs->personArray[ret].age;
        cout << "请输入电话号码： " << endl;
        cin >> Abs->personArray[ret].phonenumber;
        cout << "请输入地址： " << endl;
        cin >> Abs->personArray[ret].address;

        cout << "修改成功！" << endl;
    }
    system("pause");
    system("cls");  // 清屏
}

// 函数6：清空联系人，不需要删除记录，只要将联系人数量置为0即可
void cleanAddBook(AdressBook * Abs)
{
    Abs->Size = 0;
    cout << "通讯录已清空！" << endl;
    system("pause");
    system("cls");  // 清屏
}

// 整体框架函数
void framework()
{
    // 创建通信录实例，这里可以不写struct
    AdressBook Abs;
    Abs.Size = 0;  // 创建实例时初始化数值

    int selection = 0;              // 用于接受用户输入
    bool keep_in_loop = true;       // 是否持续主循环

    while(keep_in_loop)
    {
        showMenu();
        cout << "请输入选项：" << endl;
        cin >> selection;

        switch (selection) 
        {
            case 1:
                // cout << "新建联系人：" << endl;
                addPerson(&Abs);
                break;
            case 2:
                // cout << "显示联系人" << endl;
                showPerson(&Abs);
                break;
            case 3:
                // cout << "删除联系人" << endl;
                removePerson(&Abs);
                break;
            case 4:
                // cout << "查找联系人" << endl;
                searchPerson(&Abs);
                break;
            case 5:
                // cout << "修改联系人" << endl;
                editPerson(&Abs);
                break;
            case 6:
                // cout << "清空通信录" << endl;
                cleanAddBook(&Abs);
                break;
            case 0:
                cout << "欢迎再次使用！" << endl;
                keep_in_loop = false;
                break;
            default:
                cout << "输入错误，请重新输入！" << endl;
                break;

        }
    }
    
}

// 是否需要显示中文？
bool ChineseDisplay = true;

int main () {
    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")

    framework ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


