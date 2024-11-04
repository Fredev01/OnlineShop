from flask import Flask, redirect, render_template, url_for, session
import pymysql
from features import settings, db
from features.core.models import Product  # Importa tu modelo de Product

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/')
def home():
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


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8000, ssl_context=('cert.pem', 'key.pem'))