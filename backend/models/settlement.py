from datetime import datetime
from extensions import db


class Settlement(db.Model):
    __tablename__ = "settlements"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False)
    farmer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    payment_id = db.Column(db.BigInteger, db.ForeignKey("payments.id"))
    blockchain_order_id = db.Column(db.BigInteger, db.ForeignKey("blockchain_orders.id"))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(
        db.Enum("PENDING", "IN_ESCROW", "RELEASED", "REFUNDED", name="settlement_status"),
        nullable=False,
        default="PENDING",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = db.relationship("Order", back_populates="settlement")
    farmer = db.relationship("User", backref=db.backref("settlements", lazy="dynamic"))
    payment = db.relationship("Payment", backref=db.backref("settlements", lazy="dynamic"))
    blockchain_order = db.relationship("BlockchainOrder", back_populates="settlement", uselist=False)

    def __repr__(self):
        return f"<Settlement order={self.order_id} status={self.status}>"
