from features import db
from features.core.models import Product  # Asegúrate de que la ruta sea correcta

def insert_initial_data():
    """Inserta datos iniciales si no existen."""
    # Crea las tablas en la base de datos
    db.create_all()

    # Verifica si ya hay productos en la base de datos
    if Product.query.count() == 0:  # Solo inserta si está vacío
        products = [
            Product(name="Smartphone XYZ", category="Electrónicaa", price=299, stock=15, image='300.png'),
            Product(name="Playera Casual", category="Ropaa", price=25, stock=50, image='playera.png'),
            # Agrega más productos según sea necesario
        ]
        db.session.bulk_save_objects(products)
        db.session.commit()
        print("Datos iniciales insertados.")
    else:
        print("Los datos iniciales ya existen.")

if __name__ == "__main__":
    # Permite ejecutar este archivo de forma independiente
    from flask import Flask
    import pymysql
    from features import settings

    pymysql.install_as_MySQLdb()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        insert_initial_data()
