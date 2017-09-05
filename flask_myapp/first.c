#include<stdio.h>
int fib(int n,int a[])
;int myfib(int n,int a[])
;
int vizstack[100]={0};
int viztop=-1;
 int vizcount=0;
int vizfound=1;
int myfib(int n,int a[])
{

int i;
int ret;
vizfound=0;
vizcount++;
printf("----\n");

printf("n=%d\n",n);

printf("a=");
for(i=0;i<sizeof(*a);i++)

printf("%d,",a[i]);
printf("\n");

printf("parent =%d\n",vizstack[viztop]);
vizstack[++viztop]=vizcount;
 ret=fib(n,a);
viztop--;
printf("----\n");

return ret;
}
//visualize
int fib(int n,int a[])
{
int ret;
if(vizfound)
{
 ret=myfib(n,a);
return ret;

}
	//printf("sizeof a=%d",sizeof(*a));
	if(n==1 || n==0)
		return n;
	return myfib(n-1,a)+myfib(n-2,a);
}
void      main()
{
	int a[4]={1,2,3,4}
	printf("size of a is=%d\n",sizeof(a)/sizeof(a[0]));
	printf("hello world using c in windows\n");
	printf("the fib of 3=%d\n",fib(5,a));


}