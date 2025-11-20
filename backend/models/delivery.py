# models/delivery.py
from extensions import db

class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(
        db.BigInteger,
        db.ForeignKey("orders.id"),
        nullable=False,
    )

    # NOTE: map to existing DB column "deliveryPartnerId"
    delivery_partner_id = db.Column(
        "deliveryPartnerId",          # <-- actual column name in MySQL
        db.BigInteger,
        db.ForeignKey("users.id"),
        nullable=True,
    )

    status = db.Column(
        db.Enum("ASSIGNED", "ACCEPTED", "PICKED_UP", "ON_THE_WAY", "DELIVERED"),
        nullable=False,
        default="ASSIGNED",
    )

    proof_image_url = db.Column(db.String(255), nullable=True)
    proof_hash_on_chain = db.Column(db.String(191), nullable=True)

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # ---------- relationships ----------

    order = db.relationship(
        "Order",
        back_populates="delivery",
        foreign_keys=[order_id],
        uselist=False,
    )

    delivery_partner = db.relationship(
        "User",
        back_populates="deliveries",
        foreign_keys=[delivery_partner_id],
    )

    def __repr__(self):
        return (
            f"<Delivery order={self.order_id} "
            f"partner={self.delivery_partner_id} status={self.status}>"
        )
