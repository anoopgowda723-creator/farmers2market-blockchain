from extensions import db


class BlockchainOrder(db.Model):
    __tablename__ = "blockchain_orders"

    id = db.Column(db.BigInteger, primary_key=True)

    # Link to orders.id (1 blockchain record per order)
    order_id = db.Column(
        db.BigInteger,
        db.ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    # On-chain reference (if you store it)
    onchain_order_id = db.Column(db.String(191), nullable=True)

    # Transaction hashes
    tx_hash_create = db.Column(db.String(191), nullable=True)
    tx_hash_release = db.Column(db.String(191), nullable=True)
    tx_hash_refund = db.Column(db.String(191), nullable=True)

    # Current on-chain state
    state = db.Column(
        db.Enum(
            "CREATED",
            "PAID",
            "FARMER_CONFIRMED",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "FUNDS_RELEASED",
            "REFUNDED",
            name="blockchain_order_state",
        ),
        nullable=False,
        default="CREATED",
        server_default="CREATED",
    )

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
        back_populates="blockchain_order"
    )

    def __repr__(self):
        return f"<BlockchainOrder order={self.order_id} state={self.state}>"
