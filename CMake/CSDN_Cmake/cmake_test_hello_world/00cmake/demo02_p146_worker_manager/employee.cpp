// employee.cpp

#include "employee.hpp"

Employee::Employee(int id, string name, int deptId)
{
    this->m_id = id;
    this->m_name = name;
    this->m_deptId = deptId;
}

void Employee::showInfo()
{
    cout << "职工编号： " << this->m_id 
        << "\t姓名： " << this->m_name
        << "\t岗位： " << this->getDeptName()
        << endl;
}

// 不能直接用 deptId，因为它是一个数字不是string
string Employee::getDeptName()
{
    return string("普通员工");
}


