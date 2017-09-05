from flask import *
import sys
import mystring2 as ms
app = Flask(__name__)


@app.route('/')
def main_form():
    return render_template("index3.html")
    #return '<form action="submit" id="textform" method="post" ><textarea name="text" rows="10" cols="50">Hello World!</textarea><input type="submit" value="Submit code"></form>'

@app.route('/echo2', methods=['POST'])
def submit_textarea():
    lang=request.json["select"]
    print(lang)
    code=request.json["codes"]
    print("server hit")
    
    print(code)
    """
    print(code,file=sys.stderr)
    """
    error=""
    if lang=="java":
        with open("hello.java","w") as f:
            f.write(code)
        try:
            ms.parse_java("hello.java")
        except Exception as e:
            error=str(e)
    elif lang=="c":
        with open("first.c","w") as f:
            f.write(code)
        try:
            ms.parse_c("first.c")
        except Exception as e:
            error=str(e)
    else:
        with open("first.py",'w') as f:
            f.write(code)
        try:
            ms.parse_py("first.py")
        except Exception as e:
            error=str(e)


    if not error=="":
        print("errors______________________________________________________________________________________")
        print(error)
        error=str(error)
        error=error.replace("\n","<br/>")
        return jsonify({"error":error})
    else:
        #return lang+"<br/>"+code
        return jsonify({"something":"sending something"})
    """ print("the contents of the file are______________________________________________________________",file=sys.stderr)
    f=open("hello.java","r")
    lines=f.readlines()
    print(lines,file=sys.stderr)
    f.close()
    
    return code+"<br/>"+lang
    """


if __name__ == '__main__':
    app.run(debug=True)