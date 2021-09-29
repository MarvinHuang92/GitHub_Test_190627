#include <iostream>
#include <stdlib.h>

using namespace std;

int main() {
    bool flag = false;
    cout << "Please input a bool value:" << endl;
    cin >> flag;
    cout << "Flag = " << flag << endl;

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}
