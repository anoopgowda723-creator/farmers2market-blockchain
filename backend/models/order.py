from extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.BigInteger, primary_key=True)
    order_uuid = db.Column(db.String(100), nullable=False, unique=True)

    buyer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    farmer_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    delivery_partner_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)

    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=False, default="INR")

    status = db.Column(
        db.Enum(
            "PENDING_PAYMENT",
            "PAID",
            "FARMER_CONFIRMED",
            "ASSIGNED_DELIVERY",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "COMPLETED",
            "REFUNDED",
            "CANCELLED",
            name="order_status",
        ),
        nullable=False,
        default="PENDING_PAYMENT",
        server_default="PENDING_PAYMENT",
    )

    delivery_address = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    razorpay_order_id = db.Column(db.String(191), nullable=True)
    razorpay_payment_id = db.Column(db.String(191), nullable=True)
    razorpay_signature = db.Column(db.String(255), nullable=True)
    blockchain_order_id = db.Column(db.String(191), nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=True,
    )

    # Relationships: users
    buyer = db.relationship("User", foreign_keys=[buyer_id], backref="buyer_orders")
    farmer = db.relationship("User", foreign_keys=[farmer_id], backref="farmer_orders")
    delivery_partner = db.relationship(
        "User", foreign_keys=[delivery_partner_id], backref="delivery_orders"
    )

    # One order → many items
    items = db.relationship(
        "OrderItem",
        back_populates="order",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # 🔴 New: one order → one delivery record
    delivery = db.relationship(
        "Delivery",
        back_populates="order",
        uselist=False
    )

    payment = db.relationship(
        "Payment",
        back_populates="order",
        uselist=False
    )

    settlement = db.relationship(
        "Settlement",
        back_populates="order",
        uselist=False
    )

    blockchain_order = db.relationship(
        "BlockchainOrder",
        back_populates="order",
        uselist=False
    )


    disputes = db.relationship(
        "Dispute",
        back_populates="order",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Order id={self.id} uuid={self.order_uuid} status={self.status}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id"), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
    order = db.relationship("Order", back_populates="items")

    # This must match Product.order_items
    product = db.relationship("Product", back_populates="order_items")

    def __repr__(self):
        return (
            f"<OrderItem order={self.order_id} "
            f"product={self.product_id} qty={self.quantity}>"
        )
