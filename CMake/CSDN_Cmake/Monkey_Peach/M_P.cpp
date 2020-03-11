#include <iostream>
#include <stdlib.h>
using namespace std;
int returnPeach(int day, int peach)
{
    if(day > 1)
    {
        peach = peach * 2 + 2;
                day -= 1;
        return returnPeach(day, peach);
    }
    else
    {
        return peach;
    }
}
int main(void)
{
    int peach = returnPeach(10,1);
    cout<<"第一天共摘桃子的数量为："<<peach<<endl;

    system("pause");
    return 0;
}