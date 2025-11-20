from extensions import db


class Settlement(db.Model):
    __tablename__ = "settlements"

    id = db.Column(db.BigInteger, primary_key=True)

    # one settlement per order
    order_id = db.Column(
        db.BigInteger,
        db.ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    # farmer who receives the settlement
    farmer_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id"),
        nullable=False
    )

    amount = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(
        db.Enum(
            "PENDING",
            "RELEASED",
            "REFUNDED",
            "FAILED",
            name="settlement_status",
        ),
        nullable=False,
        default="PENDING",
        server_default="PENDING",
    )

    tx_hash_release = db.Column(db.String(191), nullable=True)
    tx_hash_refund = db.Column(db.String(191), nullable=True)

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

    # 🔗 Relationships
    order = db.relationship(
        "Order",
        back_populates="settlement"
    )

    farmer = db.relationship(
        "User",
        foreign_keys=[farmer_id]
        # no backref here to avoid clashes; you can add
        # a relationship in User if you want later
    )

    def __repr__(self):
        return f"<Settlement order={self.order_id} farmer={self.farmer_id} status={self.status}>"
