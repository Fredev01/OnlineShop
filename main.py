from flask import Flask, redirect, render_template, url_for, session
import pymysql
from features import settings
from features import db
from features import auth_route, auth_api

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(auth_api)
app.register_blueprint(auth_route)
@app.route('/')
def home():
    """Displays a Page based on the session of the current user

    Returns:
        html template: Returns the Dashboard or Index
    """
    if 'username' in session:
        return redirect(url_for('dashboard'))
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