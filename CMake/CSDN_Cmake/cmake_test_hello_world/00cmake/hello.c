//hello.c
#include <stdio.h>
int main(){
 puts("hello, world!");
 
 # ifdef ADD_DEFINITION
 puts("\nMACRO ADD_DEFINITION is added.");
 # endif
 
 getchar();
 return 0;
}