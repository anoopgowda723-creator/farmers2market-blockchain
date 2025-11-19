from datetime import datetime
from extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.BigInteger, primary_key=True)
    order_uuid = db.Column(db.String(36), unique=True, nullable=False)
    buyer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    farmer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    delivery_partner_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=False, default="INR")
    status = db.Column(
        db.Enum(
            "PENDING_PAYMENT",
            "PAID",
            "FARMER_CONFIRMED",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "COMPLETED",
            "CANCELLED",
            "DISPUTED",
            "REFUNDED",
            name="order_status",
        ),
        nullable=False,
        default="PENDING_PAYMENT",
    )
    delivery_address = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    buyer = db.relationship("User", foreign_keys=[buyer_id], back_populates="orders_as_buyer")
    farmer = db.relationship("User", foreign_keys=[farmer_id], back_populates="orders_as_farmer")
    delivery_partner = db.relationship("User", foreign_keys=[delivery_partner_id], backref="orders_as_delivery")

    items = db.relationship("OrderItem", back_populates="order", lazy="dynamic", cascade="all, delete-orphan")
    payment = db.relationship("Payment", back_populates="order", uselist=False)
    settlement = db.relationship("Settlement", back_populates="order", uselist=False)
    blockchain_order = db.relationship("BlockchainOrder", back_populates="order", uselist=False)
    delivery = db.relationship("Delivery", back_populates="order", uselist=False)
    disputes = db.relationship("Dispute", back_populates="order", lazy="dynamic")

    def __repr__(self):
        return f"<Order {self.id} {self.order_uuid} status={self.status}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id} qty={self.quantity}>"
