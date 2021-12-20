import mysql.connector
from flask import Flask,flash,redirect,url_for,request,render_template
import os
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

counter = 0

mydb = mysql.connector.connect(host= "localhost",user = "root",passwd = "1S1XLCFN",database = "exam")
mycursor = mydb.cursor(buffered=True)


@app.route('/teacher',methods = ["POST","GET"])
def teacher():
	return render_template("teacherLogin.html",message = "")

@app.route('/student',methods = ["POST","GET"])
def student():
	return render_template("studentLogin.html",message = "")




@app.route('/CreateQuestion', methods = ['POST','GET'])  
def CreateQuestion():
	global counter 
	counter += 1

	f = request.files["question"]
	que_path = os.path.join('static', f.filename)
	f.save(que_path)

	option1 = request.form['option1']
	option2 = request.form['option2']
	option3 = request.form['option3']
	option4 = request.form['option4']

	answer = request.form['answer']

	subject = "test"

	tmp = que_path[6::1]

	que_path = tmp

	query = f"INSERT INTO {subject} VALUES({counter},'{que_path}','{option1}','{option2}','{option3}','{option4}','{answer}');"

	#INSERT INTO SUBJECT VALUES(counter,'que_path','option1','option2','option3','option4','answer');

	mycursor.execute(query)
	mycursor.execute("COMMIT")

	return render_template("menu.html")

@app.route("/check_teacher_credentials" ,methods = ["POST","GET"])
def check_teacher_credentials():
	#processing
	email = request.form["email"]
	password = request.form["password"]

	print(email+" "+password)
	# teacher(email,pa)
	mycursor.execute("select * from teacher")

	for i in mycursor:
		if i[0]==email and i[1]==password:
			return render_template("menu.html")
	

	return render_template("teacherLogin.html",message="Either password or email didnot match inour database")


# for teacher section

@app.route("/callQuestionAdd",methods = ["POST","GET"])
def callQuestionAdd():
	return render_template("questionAdd.html")

@app.route("/callQuestionRead", methods=["POST", "GET"])
def callQuestionRead():
	mycursor.execute("select * from test")

	question_paper = []

	for i in mycursor:
		question_paper.append(i)

	number_of_questions = len(question_paper)

	return render_template("questionRead.html", question_paper=question_paper,noq = number_of_questions)

@app.route("/deleteQue", methods=["POST", "GET"])
def deleteQue():

	qid = request.form['qid']

	mycursor.execute(f"delete from test where id = {qid}")
	mycursor.execute("commit")

	return render_template("menu.html")

@app.route("/callQuestionDelete", methods=["POST", "GET"])
def callQuestionDelete():

	mycursor.execute("select * from test;")

	question_paper = []

	for i in mycursor:
		question_paper.append(i)

	number_of_questions = len(question_paper)
	
	return render_template("delete_sheet.html",question_paper = question_paper,noq = number_of_questions)



# for authentication

@app.route("/check_student_credentials" ,methods = ["POST","GET"])
def check_student_credentials():
	#processing
	PRN = request.form["prn"]
	password =request.form['password']

	mycursor.execute("select * from student")

	found = False
	for i in mycursor:
		if i[0]==PRN and i[1]==password:
			found =True
	
	if found == False:
		return render_template("studentLogin.html",message="Either password or email didnot match inour database")

	mycursor.execute("select * from test;")

	question_paper = []

	for i in mycursor:
		question_paper.append(i)

	number_of_questions = len(question_paper)
	
	return render_template("exam_sheet.html",question_paper = question_paper, PRN = PRN,noq = number_of_questions)


	
@app.route("/complete", methods = ["POST","GET"])
def complete():
	marks_obtained = 0

	mycursor.execute("select * from test")

	question_paper = []

	for i in mycursor:
		question_paper.append(i)

	number_of_questions = len(question_paper)

	for i in range(0,number_of_questions):	

		try:
			x = request.form[((str)(question_paper[i][0]))]
		except:
			continue

		print(question_paper[i][((int) (x))] + " " + question_paper[i][6])

		if question_paper[i][((int) (x))] == question_paper[i][6]:
			marks_obtained += 1
	
	prn = request.form['prn']
	# print(type(prn))
	mycursor.execute("update student set marks= "+(str)(marks_obtained)+" where prn ="+ prn+";")
	mycursor.execute("COMMIT")
	return "Congrats you scored " + (str)(marks_obtained) + " marks"

@app.route("/")
def home():
	return render_template("userType.html")

app.run(debug=True)
