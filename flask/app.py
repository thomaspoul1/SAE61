from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

#infos DB
app.config['MYSQL_HOST'] = 'mariadb'
app.config['MYSQL_USER'] = 'sae61'
app.config['MYSQL_PASSWORD'] = 'sae61'
app.config['MYSQL_DB'] = 'sae61'

mysql = MySQL(app)

@app.route("/")
def accueil():
    return render_template('index.html')

##############################


@app.route("/inscription", methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        Users = request.form
        identifiant = Users['identifiant']
        mail = Users['email']
        password = Users['mdp']

        # Regex pour les contraintes d'identifiant
        if not re.match(r'^[a-z]{6,10}$', identifiant):
            return "L'identifiant doit contenir entre 6 et 10 caractères en minuscules uniquement." 

        # Regex pour les contraintes de mail
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail):
            return "L'adresse e-mail est invalide." 

        # Regex pour les contraintes de mot de passe
        if not re.match(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[#$%{}@])[a-zA-Z0-9#$%{}@]{6,15}$', password): 
            return "Le mot de passe doit contenir entre 6 et 15 caractères, au moins 1 chiffre, au moins 1 majuscule, au moins 1 minuscule et au moins 1 caractère parmi #%{}@."

        cur = mysql.connection.cursor()

        # Vérifier si l'identifiant est déjà utilisé
        cur.execute("SELECT COUNT(*) FROM Utilisateurs WHERE identifiant = %s", (identifiant,))
        if cur.fetchone()[0] > 0:
            cur.close()
            return "Cet identifiant est déjà utilisé. Veuillez en choisir un autre."
        
        # Vérifier si l'adresse email est déjà utilisée
        cur.execute("SELECT COUNT(*) FROM Utilisateurs WHERE mail = %s", (mail,))
        if cur.fetchone()[0] > 0:
            cur.close()
            return "Cette adresse e-mail est déjà utilisée. Veuillez en choisir une autre."

        # Insertion des données sans hashage du mot de passe
        cur.execute("INSERT INTO Utilisateurs(identifiant, mail, password) VALUES (%s, %s, %s)", (identifiant, mail, password))
        mysql.connection.commit()
        cur.close()
        return "Félicitations ! Vous êtes inscrits."
    return render_template('inscription.html')

##############################

@app.route("/connexion", methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        Users = request.form
        identifiant = Users['identifiant']
        password = Users['mdp']
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM Utilisateurs WHERE identifiant = %s", (identifiant,))
        user_password = cur.fetchone()
        cur.close()
        if user_password:
            if user_password[0] == password:
                return f"Bonjour {identifiant}!"
            else:
                return "Connexion échouée, vérifiez votre mot de passe"
        else:
            return "Identifiant ou mot de passe incorrect"
    return render_template('connexion.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
