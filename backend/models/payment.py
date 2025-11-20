from extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.BigInteger, primary_key=True)

    order_id = db.Column(
        db.BigInteger,
        db.ForeignKey("orders.id"),
        nullable=False,
        unique=True  # 1 payment record per order
    )

    transaction_status = db.Column(
        db.Enum("CREATED", "SUCCESS", "FAILED", "REFUNDED", name="payment_status"),
        nullable=False,
        default="CREATED",
        server_default="CREATED",
    )

    razorpay_order_id = db.Column(db.String(191), nullable=True)
    razorpay_payment_id = db.Column(db.String(191), nullable=True)
    razorpay_signature = db.Column(db.String(255), nullable=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=True
    )

    # 🔗 Relationship back to Order
    order = db.relationship(
        "Order",
        back_populates="payment"
    )

    def __repr__(self):
        return f"<Payment order={self.order_id} status={self.transaction_status}>"
