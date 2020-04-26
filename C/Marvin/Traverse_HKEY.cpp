/* Traverse all HKEY in reg, and print their values. */

//#include "stdafx.h"  //just remove this include if it cannot be found in local machine.
#include <stdio.h> 
#include <time.h> 
#include <windows.h> 
 
HKEY hKey[] = 
{
	HKEY_CLASSES_ROOT, 
    HKEY_CURRENT_USER, 
    HKEY_LOCAL_MACHINE, 
    HKEY_USERS, 
	HKEY_CURRENT_CONFIG
}; 
const char *sKey[] = 
{
	"HEKY_CLASSES_ROOT", 
    "HEKY_CURRENT_USER", 
    "HEKY_LOCAL_MACHINE", 
    "HEKY_USERS", 
    "HEKY_CURRENT_CONFIG"
}; 
 
char data_set[1024]; 
DWORD nCount = 0;  // calculate the keys number 
 
void EnumValue(HKEY	hKey) 
{ 
	int dwIndex = 0; 
	char valuename[MAX_PATH + 1]; 
	DWORD valuenamelen; 
	DWORD Type; 
	union
	{ 
		BYTE data[1024]; 
		DWORD idata; 
	}lpdata; 
	DWORD datalen; 
 
	valuenamelen = sizeof(valuename); 
	datalen = sizeof(lpdata); 
	memset(&lpdata, 0, sizeof(lpdata)); 

	while(::RegEnumValue (hKey, dwIndex, (LPTSTR)valuename,	&valuenamelen, 0, &Type, lpdata.data, &datalen) != ERROR_NO_MORE_ITEMS) 
	{ 
		switch(Type) 
		{ 
			case REG_SZ: 
				printf("value:\t%s\tdata:\t%s\n", valuename, (char*)lpdata.data); 
				break; 
			case REG_DWORD: 
				printf("value:\t%sdata:\t%ld\n", valuename, lpdata.idata); 
				break; 
			default: 
				break; 
		} 

		dwIndex ++; 
		valuenamelen = sizeof(valuename); 
		datalen = sizeof(lpdata); 
		memset(&lpdata, 0, sizeof(lpdata)); 
	} 
 
} 
 
void EnumKey(HKEY hKey, const char *sKey) 
{ 
	HKEY h; 
	int dwIndex = 0; 
 
	char strkey[2048]; 
	char name[1024] = {0}; 
	DWORD namelen = sizeof(name); 
	FILETIME ftLastWriteTime; 
	//printf("befor RegOpenKeyEx data_set is %s!\n", data_set);
 
	if(::RegOpenKeyEx(hKey, (LPTSTR)data_set, 0, KEY_READ, &h) != ERROR_SUCCESS) 
	{ 
		//printf("can't open key %s!\n", strkey); 
		//printf("can't open key %s!\n", sKey); 
		return; 
	} 
	printf("open key %s ok!\n", sKey);
	//printf("after RegOpenKeyEx data_set is %s!\n", data_set);
	while(::RegEnumKeyEx(h, dwIndex, name, &namelen, 0, NULL, NULL, &ftLastWriteTime) != ERROR_NO_MORE_ITEMS) 
	{ 
		EnumValue(h); 
		nCount ++; 
		//printf("%s\\%s\n ", sKey, name);
		//strcpy(name, "\\");
		Sleep(100); 
		HKEY hk;
 
		if(::RegOpenKeyEx(h, (LPTSTR)name, 0, KEY_READ, &hk) == ERROR_SUCCESS) 
		{
			strcpy(data_set, ""); 
			strcpy(strkey, sKey); 
			strcat(strkey, "\\"); 
			strcat(strkey, name);
			//printf("--view item %s success!\n", strkey);
			EnumKey(hk, strkey); 
			::RegCloseKey(hk); 
		} 
		dwIndex += 1; 
		namelen = sizeof(name);	 //must be specified every time!!! 
	} 
	::RegCloseKey (hKey); 
} 
 
int main() 
{ 
	//freopen("out.txt", "w", stdout);  //redirect standard output to file "out.txt"
	printf("Enum all reg keys and values\n"); 
	time_t	start, end; 
	time(&start); 
	//for(int i = 0; i < 5; i++) 
	//{ 
		//strcpy(data_set, " "); 
		//EnumKey(hKey[i], sKey[i]); 
		EnumKey(HKEY_LOCAL_MACHINE, "HEKY_LOCAL_MACHINE");
	//} 
	time(&end); 
	printf("altogether %ld keys!!!\n", nCount); 
	printf("using time: %ld seconds!\n", end - start); 

	//fclose(stdout);  //close file "out.txt"
	return 0;
}

