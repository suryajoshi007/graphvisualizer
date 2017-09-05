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
    lang=request.form["select"]
    code=request.form["codes"]
    
    return code+"<br/>"+lang


if __name__ == '__main__':
    app.run()