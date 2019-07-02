#include <stdio.h>
#define IN 1 /* inside a word */
#define OUT 0 /* outside a word */

/* count lines, words, and characters in input 统计输入的字符数、单词数、行数*/
int main()
{
	int c, nl, nw, nc, state;
	state = OUT;
	nl = nw = nc = 0;

	while ((c = getchar()) != EOF) {
		++nc;										//总字符数
		if (c == '\n')								//遇到换行符，行数+1
			++nl;
		if (c == ' ' || c == '\n' || c == '\t')		//遇到空格或换行或制表符，表示离开了上一个单词
			state = OUT;
		else if (state == OUT) {
			state = IN;
			++nw;									//当不是上述三种特殊字符时，认为进入新单词，单词数+1
		}
	}
	printf("lines: %d\nwords: %d\ncharacters: %d\n", nl, nw, nc);
	getchar();
}