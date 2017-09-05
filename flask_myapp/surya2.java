import java.util.*;
class surya2
{

static int vizcount=0;
static Stack st;
static boolean vizfound=true;
public static void main(String args[])
{

st=new Stack();
st.push(0);
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

public static void mytoh(int s,int t,int d,int n)
{
vizfound=false;
vizcount++;
System.out.println("start----");

System.out.println("s="+s);

System.out.println("t="+t);

System.out.println("d="+d);

System.out.println("n="+n);

System.out.println("parent ="+st.peek());
st.push(vizcount);
  toh(s,t,d,n);
st.pop();
System.out.println("stop----");
return;

}
public static void toh(int s,int t,int d,int n)
{
if(vizfound){  mytoh(s,t,d,n);

return;
}if(n==0)
return;
mytoh(s,d,t,n-1);
System.out.println("move ring "+n+" from "+s+" to "+d);
mytoh(t,s,d,n-1);
}
}

