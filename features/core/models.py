from features.core.db import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    image = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "image": self.image
        }
