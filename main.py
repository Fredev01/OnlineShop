from flask import Flask, redirect, render_template, url_for, session, request
import pymysql, os
from authlib.integrations.flask_client import OAuth
from features import settings, db, auth_route, auth_api, UserCU
from features.core.models import Product  # Importa tu modelo de Product
from dotenv import load_dotenv
from email.message import EmailMessage  # Importa EmailMessage aquí
import smtplib, ssl

pymysql.install_as_MySQLdb()
load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# Registrar blueprints
app.register_blueprint(auth_api)
app.register_blueprint(auth_route)

@app.route('/')
def home():
    """Displays a Page based on the session of the current user"""
    if 'username' in session:
        return redirect(url_for('list_products'))
    return render_template('login.html')


@app.route('/products')
def list_products():
    """Displays a Page with a list of products"""
    products = Product.query.all()  # Assuming Product is a SQLAlchemy model

    # Convert products to a list of dictionaries
    serialized_products = [
        {
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "stock": product.stock,
            "image": url_for('static', filename=f'img/{product.image}')
        }
        for product in products
    ]

    return render_template('search.html', products=serialized_products)

@app.route("/login/google")
def login_google():
    try:
        redirect_uri = url_for("authorize_google", _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as err:
        print(err)
        return "Error occurred during login with Google", 500

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
        return redirect(url_for('list_products'))
    except Exception as err:
        print(err)
        return "Error occurred during login with Google", 500

@app.route('/contact')
def contact():
    """Displays the contact form page."""
    return render_template('contactanos.html')  # Asegúrate de tener este template creado

def send_email(email_sender, email_receiver, subject, body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, 'izqtoxhdvxnipoky')   
        smtp.sendmail(email_sender, email_receiver, em.as_string())

@app.route("/send_email", methods=["POST"])
def trigger_email():
    email_sender = request.form["email_sender"]
    email_receiver = request.form.get("email_receiver", os.getenv("USER_SEND_GMAIL"))
    subject = request.form["subject"]
    body = request.form["body"]

    send_email(email_sender, email_receiver, subject, body)
    return redirect(url_for('contact', success=True))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8000, ssl_context=('cert.pem', 'key.pem'))
