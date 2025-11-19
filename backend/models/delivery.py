from datetime import datetime
from extensions import db


class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False, unique=True)
    delivery_partner_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(
        db.Enum(
            "ASSIGNED",
            "ACCEPTED",
            "PICKED_UP",
            "ON_THE_WAY",
            "DELIVERED",
            "FAILED",
            name="delivery_status",
        ),
        nullable=False,
        default="ASSIGNED",
    )
    proof_hash = db.Column(db.String(255))
    proof_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = db.relationship("Order", back_populates="delivery")
    delivery_partner = db.relationship("User", back_populates="deliveries")

    def __repr__(self):
        return f"<Delivery order={self.order_id} status={self.status}>"
