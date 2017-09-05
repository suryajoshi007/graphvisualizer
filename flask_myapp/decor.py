import pydot 
import graphviz as gv
from PIL import Image

stack=[0]
count=0
callers=[]
calldict={}

#g=gv.Digraph(format='png')
g=pydot.Dot(graph_type="graph")


def addnodetograph(name):
	global g
	g.node(name)

def drawedge():
	global g
	for id,nodedata in calldict.items():
		parent=nodedata
		print("args")
		print(parent.args)
		for child in parent.children:
			#g.edge(id,child,str(calldict[child].ret))#,"ret "+str(child.ret))
			g.add_edge(pydot.Edge(pydot.Node(id),pydot.Node(child),label=str(calldict[child].ret)))

class nodedata(object):
	def __init__(self,funcname,*args):
		self.funcname=funcname
		self.args=args
		self.children=[]
		self.ret=0

calldict['0']=nodedata("main","main")

class decor(object):
	def __init__(self,funcname):
		self.funcname=funcname

	def __call__(self,*args):
		global count,stack,g
		parent=str(stack[-1])
		count+=1
		child=str(count)
		calldict[child]=nodedata(self.funcname,*args)
		calldict[parent].children.append(child)
		stack.append(count)
		#g.node(child,",".join(map(str,args)))
		g.add_node(pydot.Node(child,label=",".join(map(str,args))))
		print(stack)
		ret=self.funcname(*args)
		calldict[child].ret=ret
		stack.pop()
		
		return ret

@decor
def fact(n):
	print("in fact function")
	if n==1:
		return n
	return n*fact(n-1)

@decor
def fib(n):
	if n==1 or n==0:
		return n
	return fib(n-1)+fib(n-2)

@decor
def gcd(m,n):
	if n==1 or n==0:
		return m
	return gcd(n,m%n)


def build_graph():
	drawedge()
	g.write_png('static/g.png')
	img=Image.open("static/g.png")
	img.show()


def main():
	print("the gcd is"+str(fib(9)))
	
	

if __name__=="__main__":
	main()

build_graph()