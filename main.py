from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import time
import sqlite3

# Initialize the Flask web app and assign a secret key
app = Flask(__name__, template_folder='templates')
app.secret_key = "DvgcehifjjbzdDF>EUGIHF"

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Action: Cette méthode renvoie le visuel de la page d'authentification
    Paramètre: Aucun
    Type: (template html)
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
                print(f"Utilisateur {username} connecté avec le token {emp[2]}")
                return redirect(url_for('page_accueil'))
            else:
                msg = 'Nom d\'utilisateur/mot de passe incorrect !'
        except sqlite3.Error as e:
            print("Erreur SQLite:", e)
        finally:
            co.close()

    return render_template('login.html', msg=msg)

@app.route('/page_accueil')
def page_accueil():
    """
    Action: Renvoie le visuel de la page d'accueil
    
    Paramètres d'entrée:
        Aucun

    Valeur de retour:
        (template html)
    """
    token = session.get('token')
    return render_template('page_accueil.html', token=token)

@app.route('/journal/<int:tokenUtilisateur>')
def journal(tokenUtilisateur):
    """
    Action: Renvoie le visuel de la page du journal intime pour y ajouter une nouvelle entrée

    Paramètres d'entrée:
        tokenUtilisateur (int)

    Valeur de retour:
        (template html)
    """
    co = sqlite3.connect('db/entry.db')
    cursor = co.cursor()
    titre, contenu, date = getDerniereEntree(tokenUtilisateur)
    co.close()
    return render_template('journal.html', title=titre, content=contenu, date=date)

def getDerniereEntree(tokenUtilisateur):
    """
    Action: Renvoie la dernière entrée du journal

    Paramètres d'entrée:
        tokenUtilisateur (int)

    Valeur de retour:
        Dernière entrée (tuple)
    """
    liste = getEntreeJournal(tokenUtilisateur)
    if liste:
        print("Element : "+str(liste[0]))
        return liste[0]
    else:
        return None

def getEntreeJournal(tokenUtilisateur):
    """
    Action: Renvoie toutes les entrées du journal intime créées par l'utilisateur

    Paramètres d'entrée:
        tokenUtilisateur (int)

    Valeur de retour:
        listeEntrees (list[tuple])
    """
    listeEntrees = []
    co = sqlite3.connect("db/entry.db")
    curs = co.cursor()
    try:
        curs.execute("SELECT titre, contenu, date FROM entry WHERE token = ? ORDER BY date DESC", (tokenUtilisateur,))
        listeEntrees = curs.fetchall()
    except sqlite3.Error as e:
        print("Erreur SQLite:", e)
    finally:
        co.close()
    return listeEntrees

@app.route('/creerNouvelleEntree', methods=['POST'])
def creerNouvelleEntree():
    """
    Action: Créer une nouvelle entrée au journal en insérant les données dans la base de données

    Paramètres d'entrée:
        Aucun

    Valeur de retour:
        Aucun
    """
    titre = request.form['title']
    contenu = request.form['content']
    tokenUti = session.get('token')
    dateActuelle = datetime.datetime.now().strftime("%Y-%m-%d")

    if titre and contenu:
        co = sqlite3.connect('db/entry.db')
        curs = co.cursor()
        try:
            curs.execute("SELECT id FROM entry ORDER BY id DESC LIMIT 1")
            dernierId = curs.fetchone()[0] + 1 if curs.fetchone() else 1
            curs.execute("INSERT INTO entry VALUES (?,?,?,?,?)", (dernierId, tokenUti, titre, contenu, dateActuelle))
            co.commit()
        except sqlite3.Error as e:
            print("Erreur SQLite:", e)
        finally:
            co.close()
        return redirect(url_for('journal', tokenUtilisateur=tokenUti))
    else:
        print("Il manque des valeurs")
        return redirect(url_for('journal', tokenUtilisateur=tokenUti))

# When the Python interpreter runs, this line executes the web app with the attributes below
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")