#include<stdio.h>

//visualize
int fib(int n,int a[])
{
	//printf("sizeof a=%d",sizeof(*a));
	if(n==1 || n==0)
		return n;
	return fib(n-1,a)+fib(n-2,a);
}


void      main()
{
	int a[4]={1,2,3,4};
	printf("size of a is=%d\n",sizeof(a)/sizeof(a[0]));
	printf("hello world using c in windows\n");
	printf("the fib of 3=%d\n",fib(3,a));

}