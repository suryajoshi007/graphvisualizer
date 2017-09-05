import java.util.*;
class hello3
{

static int vizcount=0;
static Stack st;
static boolean vizfound=true;
public static void main(String args[])
{

st=new Stack();
st.push(0);
fib(5);
}
//visualize

public static int myfib(int n)
{
vizfound=false;
vizcount++;
System.out.println("----");

System.out.println("n="+n);

System.out.println("parent ="+st.peek());
st.push(vizcount);
int vizret=fib(n);
st.pop();
System.out.println("----");
return vizret;

}
public static int fib(int n)
{
if(vizfound){int vizret=myfib(n);

return vizret;
}if(n==0 || n==1)
return n;
return myfib(n-1)+ myfib(n-2);
}
}
