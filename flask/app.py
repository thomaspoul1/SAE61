from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

# Configuration de la base de données
app.config['MYSQL_HOST'] = 'mariadb'
app.config['MYSQL_USER'] = 'sae61'
app.config['MYSQL_PASSWORD'] = 'sae61'
app.config['MYSQL_DB'] = 'sae61'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('accueil.html')

@app.route("/inscription", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = request.form
        username = user_data.get('identifiant')
        email = user_data.get('email')
        password = user_data.get('mdp')

        if not re.match(r'^[a-z]{6,10}$', username):
            return "L'identifiant doit contenir entre 6 et 10 caractères en minuscules uniquement."
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "L'adresse e-mail est invalide."
        if not re.match(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[#$%{}@])[a-zA-Z0-9#$%{}@]{6,15}$', password):
            return "Le mot de passe doit contenir entre 6 et 15 caractères, incluant des chiffres, majuscules, minuscules et caractères spéciaux."

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Utilisateurs WHERE identifiant = %s", (username,))
        if cur.fetchone()[0] > 0:
            return "Cet identifiant est déjà utilisé. Veuillez en choisir un autre."
        cur.execute("SELECT COUNT(*) FROM Utilisateurs WHERE mail = %s", (email,))
        if cur.fetchone()[0] > 0:
            return "Cette adresse e-mail est déjà utilisée. Veuillez en choisir une autre."

        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO Utilisateurs (Nom, Prenom, identifiant, mail, password) VALUES (%s, %s, %s, %s, %s)",
                    (last_name, first_name, username, email, hashed_password))
        mysql.connection.commit()
        return "Félicitations ! Vous êtes inscrits."
    return render_template('inscription.html')

@app.route("/connexion", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.form
        username = user_data.get('identifiant')
        password = user_data.get('mdp')

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM Utilisateurs WHERE identifiant = %s", (username,))
        user_record = cur.fetchone()
        if user_record:
            stored_password = user_record[0]
            if check_password_hash(stored_password, password):
                return "Connexion réussie !"
            else:
                return "Connexion échouée, vérifiez votre mot de passe."
        else:
            return "Identifiant ou mot de passe incorrect."
    return render_template('connexion.html')

@app.route("/liste")
def list_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT identifiant FROM Utilisateurs")
    user_ids = cur.fetchall()
    return render_template('liste.html', user_ids=user_ids)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

