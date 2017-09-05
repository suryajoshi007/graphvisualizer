import subprocess
import os
import graphviz as gv
from PIL import Image
import pydot



def new_output_handler(text):
	g=pydot.Dot(graph_type="graph")
	print(text.split("\n"))
	text=text.split('\n')
	gdict={}
	gparent=[]
	count=0
	gparent.append(0)
	main=pydot.Node(str(count),label="main()")
	g.add_node(main)
	gdict[0]=""
	for sent in text:
		if "start----" in sent:
			count+=1
			g.add_node(pydot.Node(str(count),label="nodedata"))
			gdict[count]="" 
			gparent.append(count)
		elif "stop----" in sent:
			child=gparent[-1]
			g.add_node(pydot.Node(str(child),label=(pydot.Node(str(child)).get_label() or "")+gdict[child]))
			gparent.pop()
			parent=gparent[-1]
			g.add_edge(pydot.Edge(pydot.Node(str(parent)),pydot.Node(child)))
		else:
			gdict[gparent[-1]]+=sent
	for key,value in gdict.items():
		print(str(key)+"......"+value)
	g.write_png("g.png")
	img=Image.open("g.png")
	img.show()
def remove_extra_space(sentences):
	sentences=[' '.join(x.split())+"\n" for x in sentences]
	return sentences




#gives function name,function header,argument list and source code of file as a list
def getfuncdetails(file):
	with open(file) as f:
		sentences=f.readlines()
	#sentences.remove("\\n")
	print("sentences are>>>>>>>>>>>>>>>>>>>>>>>>")
	print(sentences)
	recindex=0

	for sent in sentences:
		if sent=="\n":
			sentences.remove(sent)
	
	print("after processing==============================")
	print(sentences)

	for sentence in sentences:
		if "//visualize" in sentence:
			recindex=sentences.index(sentence)+1
			break

	funcheader=sentences[recindex]
	for bits in funcheader.split():
		if "(" in bits:
			funcname=bits.split('(')[0]

	argind=funcheader.index('(')
	argind2=funcheader.index(')')
	args=funcheader[argind+1:argind2].strip().split(',')
	#print(args)
	#print("funcname is = "+funcname)
	arglist=[]
	for arg in args:
		if '[]' in arg.split()[1]:
			datatype='[]'
			if '[][]' in arg:
				datatype='[][]'
			dataT,var=arg.split()
			var=var.split('[')[0]
			arglist.append((dataT+datatype,var))
		else:
			datatype,var=arg.split()
			arglist.append((datatype,var))

	#print(arglist)
	return funcname,funcheader,arglist,sentences

def findindex(sentences,pat,nopat="^^^"):
	for sent in sentences:
		if pat in sent and nopat not in sent:
			return sentences.index(sent)+1

def findfunc(sentences,funcname):
	for sent in sentences:
		if funcname in sent:
			fstart=sentences.index(sent)
			break;
	count=0
	linecount=0
	for sent in sentences[fstart:]:
		print("count="+str(count))
		if '{' in sent:
			count+=1
		if '}' in sent:
			count-=1
			if count==0:
				break
		linecount+=1

	return fstart,fstart+linecount

def insertargjava(sentences,arg_ip,arglist):
	for (datatype,var) in arglist:
		#print(datatype,var)
		if "[]" in datatype:
			if "[][]" not in datatype:
				argstmt="\nSystem.out.print(\""+var+"=\");\nfor(int i=0;i<"+var+".length;i++)\n{\nSystem.out.print("+var+"[i]+\",\");\n}\nSystem.out.println();\n"
			elif "[][]" in datatype:
				argstmt="\nSystem.out.println(\""+var+"\");\n"
		else:
			argstmt="\nSystem.out.println(\""+var+"=\"+"+var+");\n"
			if "String"==datatype.strip():
				argstmt="\nSystem.out.print(\""+var+"=\");\nfor(int i=0;i<"+var+".length();i++)\n{\nSystem.out.print("+var+".charAt(i)+\",\");\n}\nSystem.out.println();\n"
		sentences.insert(arg_ip,argstmt)
		arg_ip+=1
	return arg_ip


def getrettype(funcheader):
	rettokens=funcheader.split()
	rettype=''
	for tokens in rettokens:
		found=False          
		for ty in ['String','int','char','void']:
			if ty in tokens:
				rettype=tokens
				found=True
				break
		if found:
			break
	#print(rettype)
	return rettype


def draw_graph(output):
	#g=gv.Graph(format='png')
	g=pydot.Dot(graph_type="graph")
	nodes=output.split('----')
	print(nodes)
	count=0
	#g.node("0","main()")
	mainnode=pydot.Node("0",label="main()")
	g.add_node(mainnode)
	for node in nodes:
		print(node)
		if "parent =" in node:
			node=node.split("\r\n")
			node.remove('')
			#print(node)
			if len(node)!=0 and node[0]!='':
				#print(node)
				count+=1
				strin=''
				child="0"
				parent="0"
				for n in node:
					if n!='':
						if "parent =" in n:
							parent=n.split('=')[1]
							child=str(count)
						else:
							strin+=n+"  "
				
				#g.node(child,strin)
				g.add_node(pydot.Node(child,label=strin))
				g.add_edge(pydot.Edge(pydot.Node(parent),pydot.Node(child)))
	#g.render('img/g')
	g.write_png("static/g.png")
	img=Image.open('static/g.png')
	#img=img.resize((100,100))
	img.show()


def parse_java(javafile):
	funcname,funcheader,arglist,sentences=getfuncdetails(javafile)
	sentences= remove_extra_space(sentences)
	myfuncheader=funcheader.replace(funcname,'my'+funcname)
	#print(myfuncheader)
	print("extra space removal____________________________________________________________")
	print(sentences)
	mainstart,mainstop=findfunc(sentences,"public static void main")
	print(mainstart)
	print(mainstop)
	start=0
	stop=prev=0
	while stop<len(sentences):
		print(">>>>>>>>>>>>>>classes") 
		try:
			prev=stop
			start,stop=findfunc(sentences[stop:],"class")
			start+=prev
			stop+=prev
			print(start)
			print(stop)
			if start<mainstart and mainstop<stop:
				print(start)
				print(sentences[start])
				classsent=sentences[start]
				print(classsent)
				break
		except:
			break 
		#print(''.join(sentences[start:stop]))
	classsent=classsent.split()
	cla_index=classsent.index("class")+1
	classname=classsent[cla_index].strip()
	if '{' in classname:
		classname=classname.split('{')[0]


	imp_ip=0;
	found=False
	for sent in sentences:
		if "import java.util.*" in sent:
			found=True
			break 
	if not found:
		sentences.insert(0,"import java.util.*; ")

	main_ip=findindex(sentences,"public static void main")
	#print(main_ip)
	main_ip=findindex(sentences[main_ip:],"{","}")+main_ip
	sent="\nst=new Stack();\nst.push(0);\n"
	sentences.insert(main_ip,sent)
	sent="\nstatic int vizcount=0;\nstatic Stack st;\nstatic boolean vizfound=true;\n"
	class_ip=findindex(sentences,"class "+classname)
	#print(class_ip)
	class_ip=findindex(sentences[class_ip:],"{","}")+class_ip
	#print(class_ip)
	sentences.insert(class_ip,sent)
	#print(''.join(sentences))
	#start,stop=findfunc(sentences,"public static void main")
	#sentences[start+1:stop]=[x.replace(funcname,'my'+funcname) for x in sentences[start+1:stop]]


	start,stop=findfunc(sentences,funcheader)
	#print("#################")
	#print(''.join(sentences[start:stop]))
	sentences[start+1:stop]=[x.replace(funcname,'my'+funcname) for x in sentences[start+1:stop]]
	#print(''.join(sentences))
	#print(arglist)
	myfunc1="\n"+myfuncheader.strip()+"\n{\nvizfound=false;\nvizcount++;\nSystem.out.println(\"start----\");\n"
	myfunc2="\nSystem.out.println(\"parent =\"+st.peek());\nst.push(vizcount);\n"
	myfunc3="\nst.pop();\nSystem.out.println(\"stop----\");"
	myfunc4="\n}\n"
	ret=myfuncheader.split()
	myfunc_ip=findindex(sentences,funcheader)-1
	sentences.insert(myfunc_ip,myfunc1)
	sentences.insert(myfunc_ip+1,myfunc2)
	sentences.insert(myfunc_ip+2,myfunc3) 
	sentences.insert(myfunc_ip+3,myfunc4)
	arg_ip=myfunc_ip+1

	myfunc_ip=insertargjava(sentences,arg_ip,arglist)
	rettype=getrettype(funcheader)
	print("function header"+funcheader)
	print("rettype "+rettype)
	argname=[]
	for _,name in arglist:
		argname.append(name)
	if rettype.strip()=="void":
		rettype=retname=" "
	else:
		retname=" vizret="
	retstmt=rettype+retname+funcname+"("+','.join(argname)+");"
	recstmt=retstmt.replace(funcname,'my'+funcname)
	#print(retstmt)
	sentences.insert(myfunc_ip+1,retstmt)
	#print(sentences[myfunc_ip+3])
	if rettype==" ":
		retstmt="\nreturn;\n"
	else:
		retstmt="\nreturn vizret;\n"
	sentences.insert(myfunc_ip+3,retstmt)
	rec_ip=findindex(sentences,funcheader)
	rec_ip=findindex(sentences[rec_ip:],"{","}")+rec_ip
	stmt="if(vizfound){"+recstmt+"\n"+retstmt+"}"
	sentences.insert(rec_ip,stmt)
	print("rettype "+rettype)
	print("recstmt "+recstmt)
	


	print("(((((((((((((((((((((((((((")

	#print(''.join(sentences))
	with open(classname+".java",'w') as f:
		f.write(''.join(sentences))
	#os.system('javac hello3.java')
	#os.system('java hello3')

	sp=subprocess.Popen("javac "+classname+".java",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,errors=sp.communicate()
	print(output)
	print(errors.decode('utf-8'))
	print(sp.returncode)
	if sp.returncode==0:
		sp=subprocess.Popen("java "+classname,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		#print("hi")
		output,errors=sp.communicate()
		#print("hello")
		print(output.decode('utf-8'))
		print(errors.decode('utf-8'))
		new_output_handler(output.decode("utf-8"))
		#draw_graph(output.decode('utf-8'))
	else:
		raise ValueError(errors)


def custom_rec_func(sentences,funcname,myfuncheader,arglist,global_ip):
	
	def getdatatype(datatype):
		if datatype.strip()=="int":
			data="%d"
		elif datatype.strip()=="char":
			data="%c"
		return data

	rettype=getrettype(myfuncheader)
	restmt=myfuncheader+"{\n"+"\nint i;\nint ret;\nvizfound=0;\nvizcount++;\nprintf(\"----\\n\");\n"
	vas=[]
	for datatype,var in arglist:
		vas.append(var)
		if '[]' in datatype:
			data=datatype.split('[')[0]
			print(data)
			data=getdatatype(data)
			stmt="\nprintf(\""+var+"=\");\nfor(i=0;i<sizeof(*"+var+");i++)\n\nprintf(\""+data+",\","+var+"[i]);\nprintf(\"\\n\");\n"
		else:
			data=getdatatype(datatype)			
			stmt="\nprintf(\""+var+"="+data+"\\n\","+var+");\n"
		restmt+=stmt
	restmt+="\nprintf(\"parent =%d\\n\",vizstack[viztop]);\nvizstack[++viztop]=vizcount;\n"
	if rettype.strip()=="void":
		returnprefix=returntype=''
		last=""
	else:
		returnprefix=rettype
		returntype=" ret="
		last="ret"

	args=','.join(vas)
	returnstatement=returntype+funcname.strip()+"("+args+");"
	restmt=restmt+returnstatement+"\nviztop--;\nprintf(\"----\\n\");\n"
	restmt+="\nreturn "+last+";\n}\n"
	sentences.insert(global_ip,restmt)
	return returnprefix+" "+last, returnstatement.replace(funcname,'my'+funcname)+"\nreturn "+last+";\n"


def parse_c(filename):
	funcname,funcheader,arglist,sentences=getfuncdetails(filename)
	remove_extra_space(sentences)
	print(funcname)
	print(funcheader)
	print(arglist)
	print(sentences)
	start,stop=findfunc(sentences,funcheader)
	sentences[start+1:stop]=[x.replace(funcname,'my'+funcname) for x in sentences[start+1:stop]]
	
	print(''.join(sentences[start:stop]))
	f=findindex(sentences[:start-1],funcheader[:funcheader.index('(')+1])
	print(f)
	global_ip=0
	for sent in sentences:
		if '#include' not in sentences:
			global_ip=sentences.index(sent)+1
			break
	myfuncheader=funcheader.replace(funcname,"my"+funcname)
	if f==None:
		sentences.insert(global_ip,myfuncheader+';')
		sentences.insert(global_ip,funcheader+';')
		global_ip+=2
	stmt="\nint vizstack[100]={0};\nint viztop=-1;\n int vizcount=0;\nint vizfound=1;\n"
	sentences.insert(global_ip,stmt)
	rec_dec,rec_func_stmt=custom_rec_func(sentences,funcname,myfuncheader,arglist,global_ip+1)
	#fib
	#start,stop=findfunc(sentences,funcname)
	stmt=rec_dec+";\nif(vizfound)\n{\n"+rec_func_stmt+"\n}\n"
	rec_ip=findindex(sentences[start:],"{","}")+start
	sentences.insert(rec_ip,stmt)
	print(start)
	print(stop)
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	sentences=''.join(sentences)
	with open('first.c','w') as f:
		f.write(sentences)
	sp=subprocess.Popen("gcc -o first first.c",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,error=sp.communicate()
	print(sp.returncode)
	if sp.returncode==0:
		sp=subprocess.Popen('first.exe',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output,error=sp.communicate()
		print(output.decode('utf-8'))
		print(output.decode('utf-8'))
		draw_graph(output.decode('utf-8'))
	else:
		raise ValueError(error)


def parse_py(filename):
	with open(filename,'r') as f:
		sentences=f.readlines()
	remove_extra_space(sentences)
	found=False
	for sent in sentences:
		if "from decor import *" in sent:
			found=True
	if found==False:
		sentences.insert(0,"from decor import *\n")
	sentences.insert(len(sentences),"\nbuild_graph()\n")
	with open("third.py",'w') as f:
		f.write(''.join(sentences))
	filename="third.py"
	sp=subprocess.Popen("python "+filename,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,error=sp.communicate()
	if not sp.returncode==0:
		raise ValueError(error)



def main():
	parse_java('surya.java')
	#parse_c('second.c')
	#parse_py('second.py')
	
if __name__=="__main__":
	main()