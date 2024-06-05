from flask import Flask, render_template

app = Flask(__name__)

#connexion a la bdd
app.config['MYSQL_HOST'] = 'mariadb'
app.config['MYSQL_USER'] = 'sae61'
app.config['MYSQL_PASSWORD'] = 'sae61'
app.config['MYSQL_DB'] = 'sae61'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/inscription", methods=['GET','POST'])
def inscription():
    return render_template('inscription.html')

@app.route("/connexion", methods=['GET','POST'])
def connexion():
    return render_template('connexion.html')

