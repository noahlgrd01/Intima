from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

#Initialise l'app. web Flask et lui attribue une clef secrète
app = Flask(__name__, template_folder='template')
app.secret_key = "DvgcehifjjbzdDF>EUGIHF"

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Action : Cette méthode renvoie le visuel de la page d'authentification
    Paramètre : Aucun
    Type : template html
    """
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

@app.route('/page_accueil')
def page_accueil():
    """
    Action : Renvoie le visuel de la page d'accueil
    
    Paramètres d'entrée :
        Aucun

    Valeur de retour :
        (html_template)
    """
    return render_template('page_accueil.html')

@app.route('/journal')
def journal():
    """
    Action : Renvoie le visuel de la page du journal intime contenant toutes les entrées créées par l'utilisateur.

    Paramètres d'entrée :
        Aucun

    Valeur de retour :
        (html_template)
    """
    return render_template('journal.html')

def getEntreeJournal(tokenUtilisateur):
    """
    Action : Renvoie le visuel de la page du journal intime contenant toutes les entrées créées par l'utilisateur.

    Paramètres d'entrée :
        token (int)

    Valeur de retour :
        listeEntrees (list[str])
    """
    listeEntrees = []
    co = sqlite3.connect("db/entry.db")
    curs = co.cursor()
    curs.execute("SELECT * FROM entry WHERE token=?", (int (tokenUtilisateur),))
    listeEntrees = curs.fetchall()

    return listeEntrees

"""
#Au lancement de l'interpreteur Python, il exécute l'app. web avec les attribus ci-dessous
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
"""

print(getEntreeJournal(1))