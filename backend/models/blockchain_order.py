from datetime import datetime
from extensions import db


class BlockchainOrder(db.Model):
    __tablename__ = "blockchain_orders"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False, unique=True)
    onchain_order_id = db.Column(db.BigInteger, nullable=False)
    contract_address = db.Column(db.String(100), nullable=False)
    buyer_address = db.Column(db.String(100), nullable=False)
    farmer_address = db.Column(db.String(100), nullable=False)
    delivery_partner_address = db.Column(db.String(100))
    escrow_amount_wei = db.Column(db.Numeric(30, 0), nullable=False)
    state = db.Column(
        db.Enum(
            "CREATED",
            "PAID",
            "FARMER_CONFIRMED",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "COMPLETED",
            "DISPUTED",
            "REFUNDED",
            name="blockchain_order_state",
        ),
        nullable=False,
        default="CREATED",
    )
    delivery_proof_hash = db.Column(db.String(255))
    last_tx_hash = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = db.relationship("Order", back_populates="blockchain_order")
    settlement = db.relationship("Settlement", back_populates="blockchain_order")

    def __repr__(self):
        return f"<BlockchainOrder order={self.order_id} state={self.state}>"
