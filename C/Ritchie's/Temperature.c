#include <stdio.h>
/* print Fahrenheit-Celsius table for fahr = 0, 20, ..., 300; floatingpoint version 摄氏度和华氏度的换算*/
int main()
{
	float fahr, celsius;
	float lower, upper, step;
	
	lower = 0; /* lower limit of temperatuire scale */
	upper = 212; /* upper limit */
	step = 2; /* step size */
	
	printf("Fahrenheit-Celsius Table\n");
	printf("Fahr Celsius\n");
	
	for (fahr = lower; fahr <= upper; fahr = fahr + step) 
	{
		celsius = (5.0 / 9.0) * (fahr - 32.0);
		printf("%3.0f %6.1f\n", fahr, celsius);
	}
	getchar();
	return 0;
}