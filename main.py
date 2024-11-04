from flask import Flask, redirect, render_template, url_for, session
from flask_wtf import CSRFProtect
import pymysql
from features import settings, db  
from dotenv import load_dotenv
import os


load_dotenv()

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Configuración de la aplicación
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")  # Carga la clave desde .env o usa un valor por defecto
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa la base de datos y la protección CSRF
db.init_app(app)
csrf = CSRFProtect(app)  # Habilita CSRF en la aplicación

@app.route('/')
def home():
    """Displays a Page based on the session of the current user

    Returns:
        html template: Returns the Dashboard or Index
    """
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8000)