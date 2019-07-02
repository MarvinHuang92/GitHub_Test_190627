#include <stdio.h>
#define MAXLINE 1000

/* 该程序将输入的多行文字中最长的一行打印出来 */

/* maximum input line length */
/* 先声明两个函数，由于getline和copy都是库中已有的函数，这里加了后缀2 */

int getline2(char line[], int maxline);
void copy2(char to[], char from[]);

/* print the longest input line */
int main()
{
	int len; /* current line length 当前的行长度*/
	int max; /* maximum length seen so far 当前最长行的长度*/
	char line[MAXLINE]; /* current input line 当前行 */
	char longest[MAXLINE]; /* longest line saved here 当前最长行 */
	
	max = 0;
	while ((len = getline2(line, MAXLINE)) > 0) //长度不是0的行，一定不是EOF，因为至少有'\0'存在
		if (len > max) {
			max = len;  //记录当前最长行的长度，用于下一次比较
			copy2(longest, line);  //保存这个最长行到一个“安全的地方”，即longest变量
		}
	if (max > 0) /* there was a line 说明至少读取了一行，避免整个输入都是空的情况*/
		printf("%s", longest);
	getchar();
	return 0;
}

/* getline: read a line into s, return length */
/* 定义getline函数，返回当前行的长度，同时对s[]数组进行操作,相当于有两个输出 */
/* 注意函数对数组的操作是直接作用在原始数组本身的，会对主调函数直接产生影响！！ */

int getline2(char s[],int lim) //定一个字符数组，和总长度限制（1000）
{
	int c, i;
	
	for (i=0; i < lim-1 && (c=getchar())!=EOF && c!='\n'; ++i) //超出1000字，或遇到换行符，或遇到EOF，停止
		s[i] = c; //将字符逐个存入数组中
	if (c == '\n') { //如果是换行符，把它也保存（在末尾）
		s[i] = c;
		++i;
	}
	
	s[i] = '\0'; //最后再放一个'\0'结尾，表示该数组完结
	return i; //输出行的长度(这个长度包括换行符和'\0'，但它并不直接呈现给用户，所以定义不用太严谨）
}

/* copy: copy 'from' into 'to'; assume to is big enough */
/* 定义copy函数，用来将最长行存储在一个单独的区域 */

void copy2(char to[], char from[]) //void表示这个函数不需要返回值
{
	int i;
	
	i = 0;
	while ((to[i] = from[i]) != '\0')  //注意前半段是赋值而不是判断，所以相当于左边的to[i]和'\0'比较
	/* 注意这里，逐个给数组的元素赋值，直接就进行了copy的操作！！ */
		++i;
}