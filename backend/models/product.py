from datetime import datetime
from extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.BigInteger, primary_key=True)
    farmer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farmer = db.relationship("User", back_populates="products")
    order_items = db.relationship("OrderItem", back_populates="product", lazy="dynamic")

    def __repr__(self):
        return f"<Product {self.id} {self.name}>"
