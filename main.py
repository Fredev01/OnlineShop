from flask import Flask, redirect, render_template, url_for, session
import pymysql
from features.core.models import Product  # Importa tu modelo de Product
from authlib.integrations.flask_client import OAuth
from features import db, auth_route, auth_api, UserCU, settings

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

db.init_app(app)


@app.route('/')
def home():
    """Displays a Page based on the session of the current user

    Returns:
        html template: Returns the Dashboard or Index
    """
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('search.html')  # Asegúrate de tener un archivo index.html en la carpeta de templates

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))


@app.route("/login/google")
def login_google():
    try:
        redirect_uri = url_for("authorize_google", _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as err:
        print(err)
        return "Error ocurred during login with google", 500



@app.route("/authorize/google")
def authorize_google():
    try:
        token = google.authorize_access_token()
        userinfo_endpoint = google.server_metadata['userinfo_endpoint']
        resp = google.get(userinfo_endpoint)
        user_info = resp.json()
        username = user_info['email']
        user_cu = UserCU()
        user_created_successfully = user_cu.create_user_without_password(username)
        if user_created_successfully:
            session['username'] = username
            session['oauth_token'] = token
        return redirect(url_for('dashboard'))
    except Exception as err:
        print(err)
        return "Error ocurred during login with google", 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8000, ssl_context=('cert.pem', 'key.pem'))