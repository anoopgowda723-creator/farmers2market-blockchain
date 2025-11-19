from datetime import datetime
from extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=False, default="INR")
    razorpay_order_id = db.Column(db.String(100), nullable=False, unique=True)
    razorpay_payment_id = db.Column(db.String(100))
    razorpay_signature = db.Column(db.String(255))
    status = db.Column(
        db.Enum("CREATED", "AUTHORIZED", "CAPTURED", "FAILED", "REFUNDED", name="payment_status"),
        nullable=False,
        default="CREATED",
    )
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = db.relationship("Order", back_populates="payment")

    def __repr__(self):
        return f"<Payment order={self.order_id} status={self.status}>"
