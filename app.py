from flask import Flask, render_template, flash, request, url_for, redirect
from content_management import Content
import sys

TOPIC_DICT = Content()

app = Flask(__name__)

# or set directly on the app
app.secret_key = 'querty'

@app.route('/')
def index() :
	return render_template("main.html")

@app.route('/dashboard/')
def dashboard() :
	return render_template("dashboard.html" , TOPIC_DICT = TOPIC_DICT )

@app.errorhandler(404)
def page_not_found(e) :
	return render_template("404.html")

@app.route('/login/', methods = ['GET', 'POST'])
def login_page() :
	error = ''
	try :
		if request.method == "POST" :
			attempted_user = request.form['username']
			attempted_password = request.form['password']
			# flash(attempted_user)
			# flash(attempted_password)
			if attempted_user == 'admin' and attempted_password == 'admin' :
				return redirect(url_for('dashboard'))
			else :
				error = "Invalid password or user"	

		return render_template("login.html", error = error)		
	except Exception as e :
		# flash(e)	
		return render_template("login.html", error = error)

if __name__ == "__main__" :
	app.run(debug=True)	
