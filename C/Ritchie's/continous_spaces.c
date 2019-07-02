#include <stdio.h>
/* 将连续多个空格改成一个空格输出 */
int main()
{
	int c;
	
	while ((c = getchar()) != EOF) { 	//检测正常字符（不是EOF的）
		if (c == ' ') { 				//检测到一个空格
			putchar(c); 				//输出这一个空格
			while (c == ' ') 			//如果接下来还是空格
				c = getchar(); 			//跳过它，读取下一个
		}
		putchar(c); 					//输出正常的字符
	}
}