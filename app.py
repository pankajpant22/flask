from flask import Flask, render_template, flash, request, url_for, redirect, session, g
from content_management import Content
from dbconnect import Connection
from pprint import pprint
from wtforms import Form, TextField, BooleanField, validators, PasswordField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
import sys
import gc

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

def login_required(f) :
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session :
			return f(*args, **kwargs)
		else :
			flash("need to log in")
			return redirect(url_for('login_page'))
	return wrap

@app.route('/logout/')
@login_required
def logout():
	session.clear()
	flash("you have been logged out")
	gc.collect()
	return redirect(url_for('dashboard'))


@app.route('/login/', methods = ['GET', 'POST'])
def login_page() :
	error = ''
	try :
		conn, cursor = Connection()
		if request.method == "POST" :
			attempted_user = request.form['username']
			attempted_password = request.form['password']
			x = cursor.execute("SELECT * FROM users WHERE username = (%s)",({thwart(attempted_user)}))
			dbPass = cursor.fetchone()[2]
			if sha256_crypt.verify(attempted_password, dbPass) :
					session['logged_in'] = True
					session['username'] = attempted_user
					flash("You are logged in")
					return redirect(url_for('dashboard'))
			else :
					error = "invalid password"

		return render_template("login.html", error = error)
	except Exception as e :
		# flash(e)
		error = "Invalid credentials"
		return render_template("login.html", error = error)

class RegisterationForm (Form) :
	username = TextField('Username',[validators.Length(min = 4, max = 20)])
	email = TextField('Email Address',[validators.Length(min = 6, max = 50)])
	password = PasswordField ('Password',[validators.Required(),
											validators.EqualTo('confirm',message = "Password not matching")])
	confirm = PasswordField('Repeat Password')

	accept_tos = BooleanField('I Accept',[validators.Required()])


@app.route('/register/', methods = ['GET', 'POST'])
def register_page() :
	try :
		form = RegisterationForm(request.form)
		if request.method == "POST" and form.validate() :
			username = form.username.data
			password = sha256_crypt.encrypt((str(form.password.data)))
			email = form.email.data

			conn, cursor = Connection()
			x = cursor.execute("SELECT * FROM users WHERE username = (%s)",({thwart(username)}))
			if int(x) > 0 :
				flash("username taken")
				return render_template('register.html', form=form)
			else :
				cursor.execute('INSERT INTO users (`username`,`password`,`email`,`tracking`) VALUES (%s, %s, %s, %s)',
				({thwart(username)},{thwart(password)},{thwart(email)},{thwart("intro")}))
				conn.commit()
				flash("Thanks for Registering")
				cursor.close()
				conn.close()
				gc.collect()
				session['logged_in'] = True
				session['username'] = username
				return redirect(url_for('dashboard'))

		return render_template("register.html", form = form)

	except Exception as e :
		return (str(e))


if __name__ == "__main__" :
	app.run(debug=True)
