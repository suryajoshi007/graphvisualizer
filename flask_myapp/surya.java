import java.util.*;
class surya2
{
public static void main(String args[])
{

System.out.println();
toh(1,2,3,3);
}

public static int fact(int n)
{
if(n==1)
return n;
return n*fact(n-1);
}

//visualize
public static void toh(int s,int t,int d,int n)
{
	if(n==0)
		return; 
	toh(s,d,t,n-1);
	System.out.println("move ring "+n+" from "+s+" to "+d);
	toh(t,s,d,n-1); 
}

}


