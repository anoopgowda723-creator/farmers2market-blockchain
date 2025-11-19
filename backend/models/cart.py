from datetime import datetime
from extensions import db


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.BigInteger, primary_key=True)
    buyer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(
        db.Enum("ACTIVE", "ORDERED", "ABANDONED", name="cart_status"),
        nullable=False,
        default="ACTIVE",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    buyer = db.relationship("User", backref=db.backref("carts", lazy="dynamic"))
    items = db.relationship("CartItem", back_populates="cart", lazy="dynamic", cascade="all, delete-orphan")


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.BigInteger, primary_key=True)
    cart_id = db.Column(db.BigInteger, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product", backref=db.backref("cart_items", lazy="dynamic"))

    def __repr__(self):
        return f"<CartItem cart={self.cart_id} product={self.product_id} qty={self.quantity}>"
