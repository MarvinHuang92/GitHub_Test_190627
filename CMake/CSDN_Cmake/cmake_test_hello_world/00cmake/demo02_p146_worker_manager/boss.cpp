// boss.cpp

#include "boss.hpp"

Boss::Boss(int id, string name, int deptId)
{
    this->m_id = id;
    this->m_name = name;
    this->m_deptId = deptId;
}

void Boss::showInfo()
{
    cout << "职工编号： " << this->m_id 
        << "\t姓名： " << this->m_name
        << "\t岗位： " << this->getDeptName()
        << endl;
}

// 不能直接用 deptId，因为它是一个数字不是string
string Boss::getDeptName()
{
    return string("老板");
}


