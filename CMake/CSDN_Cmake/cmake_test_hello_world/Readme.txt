2019-9-28

Cmake 从零开始，因为之前学的都忘了

01Make
主要参考：https://www.jb51.net/article/148903.htm
======================================================
1. 手写一个c文件hello.c
2. 手写一个Makefile
3. 在这个目录下运行cmd，输入make即可

make命令的本质是代替你输入一个稍微复杂的命令：cc hello.c -o hello
而具体这个命令的细节在Makefile规定
比如Makefile中写了CC := gcc就相当于将上面的cc编译器换成gcc：gcc hello.c -o hello
======================================================


00Cmake
主要参考：https://blog.csdn.net/kai_zone/article/details/82656964
主要参考2：https://blog.csdn.net/afei__/article/details/81201039
======================================================
由于手写Makefile比较烦，而且不能跨平台，所以用cmake命令来替你写Makefile

方法：
1. 手写一个c（这里的c沿用之前的，但加上了一行可选输出（有宏定义就会输出，否则不输出））
2. 手写一个CMakeLists.txt，注意文件名的大小写
3. 新建一个build文件夹，并且cd进去（这样可以使中间产物不和源文件混在一起，build叫什么名字无所谓，只是习惯）
4. cmd中运行cmake .. 注意两个点，它找的是CMakeLists.txt的位置，就像make找的是Makefile的位置
5. 它会自动生成一个Makefile，然后运行make即可编译出exe了

NOTE：
之前安装VS2019时候把原有的gcc编译器环境变量吃掉了，导致现在生成的不是Makefile而是sln文件
因为默认编译器变成了VS
解决方法：在第4步改用这个命令：cmake.exe .. -G "MinGW Makefiles"，之后的make照常