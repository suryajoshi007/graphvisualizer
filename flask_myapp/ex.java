import java.util.Scanner;
public class ex2
{
 static int MAX = 100;
 static final int infinity = 999;
 public static void main(String args[])
{
 int cost = infinity;
 int c[][] = {{ 999, 10, 15, 20,},
{5, 999, 9, 10},
{6, 13, 999, 12},
{8, 8, 9, 999}};
 int tour[] = new int[4]; // optimal tour
 int n=4; // max. cities
 System.out.println("Travelling Salesman Problem using Dynamic Programming\n");
 for (int i = 0; i < n; i++)
 tour[i] = i;
 cost = tspdp(c, tour, 0, n);
 // print tour cost and tour
 System.out.println("Minimum Tour Cost: " + cost);
 System.out.println("\nTour:");
 for (int i = 0; i < n; i++)
{
 System.out.print(tour[i] + " -> ");
 }
 System.out.println(tour[0] + "\n");
 //scanner.close(); 
}

//visualize
static int tspdp(int c[][], int tour[], int start, int n)
{
 int i, j, k;
 int temp[] = new int[4];
 int mintour[] = new int[4];
 int mincost;
 int cost;
 if (start == n - 2)
 return c[tour[n - 2]][tour[n - 1]] + c[tour[n - 1]][0];
 mincost = infinity;
 for (i = start + 1; i < n; i++)
{
 System.out.println("i="+i);
 for (j = 0; j < n; j++)
 temp[j] = tour[j];
 temp[start + 1] = tour[i];
 temp[i] = tour[start + 1];
 System.out.println("exchanging "+i+" and "+(start+1));
 System.out.println("comparing "+tour[start]+" and "+tour[i]);
if (c[tour[start]][tour[i]] + (cost = tspdp(c, temp, start + 1,n)) < mincost)
{
 mincost = c[tour[start]][tour[i]] + cost;
 for (k = 0; k < n; k++)
 mintour[k] = temp[k];
 }
 }
 for (i = 0; i < n; i++)
 tour[i] = mintour[i];
 return mincost;
 }
} 