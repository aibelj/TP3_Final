from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'some secret key'
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyUsers'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
def emailConfirmation(email):
    message = Mail(
        from_email='mk872@njit.edu',
        to_emails= email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>Python API Test</strong>')
    try:
        sg = SendGridAPIClient(
            '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'
        )
        message.template_id = 'd-f444ccdb493e4024a2a40de171c1acdd'
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.body)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        Email = request.form['Email']
        Password = request.form['Password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM tblMyUsers WHERE Email = %s AND Password = %s', (Email, Password))
        userTest = cur.fetchone()
        if userTest:
            session['Email'] = userTest['Email']
            session['Password'] = userTest['Password']
            return redirect("/index", code=302)
        else:
            return "Incorrect Email/Password"


    return render_template('login.html', error=error)

@app.route('/signUp',methods = ['GET','POST'])
def signUp():
    if request.method == "POST":
        details = request.form
        Email = details['Email']
        Password = details['Password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tblMyUsers(Email, Password) VALUES (%s, %s)", (Email, Password))
        mysql.connection.commit()
        cur.close()
        emailConfirmation(Email)
        return redirect("/", code=302)


    return render_template('signUp.html')

@app.route('/index')
def calendar():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)