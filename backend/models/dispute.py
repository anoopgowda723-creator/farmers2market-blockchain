from extensions import db


class Dispute(db.Model):
    __tablename__ = "disputes"

    id = db.Column(db.BigInteger, primary_key=True)

    order_id = db.Column(
        db.BigInteger,
        db.ForeignKey("orders.id"),
        nullable=False,
    )

    buyer_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    farmer_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    reason = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.Enum(
            "OPEN",
            "IN_REVIEW",
            "RESOLVED_BUYER",
            "RESOLVED_FARMER",
            "CLOSED",
            name="dispute_status",
        ),
        nullable=False,
        default="OPEN",
        server_default="OPEN",
    )

    resolution_note = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False,
    )

    resolved_at = db.Column(db.DateTime, nullable=True)

    # 🔗 Relationships

    # This matches Order.disputes
    order = db.relationship(
        "Order",
        back_populates="disputes",
    )

    # Link to users (no backref to avoid name clashes)
    buyer = db.relationship(
        "User",
        foreign_keys=[buyer_id],
    )

    farmer = db.relationship(
        "User",
        foreign_keys=[farmer_id],
    )

    def __repr__(self):
        return f"<Dispute id={self.id} order={self.order_id} status={self.status}>"
