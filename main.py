from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__, template_folder='template')
app.secret_key = "Hede8JKZd5746Iozd#74sDgzyd"
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        co = sqlite3.connect('db/id.db')
        curs = co.cursor()

        try:
            curs.execute('SELECT * FROM id WHERE username = ? AND password = ?', (username, password,))
            emp = curs.fetchone()

            if emp:
                session['id'] = emp[0]
                session['username'] = emp[1]
                session['token'] = emp[2]
                return redirect(url_for('page_accueil'))
            else:
                msg = 'Incorrect username/password!'
        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            co.close()

    return render_template('login.html')

@app.route('/page_accueil', methods=['GET', 'POST'])
def page_accueil():
    return render_template('page_accueil.html')

app.run(debug=True, host="0.0.0.0", port="5000")