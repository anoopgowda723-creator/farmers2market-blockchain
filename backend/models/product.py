from extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.BigInteger, primary_key=True)
    farmer_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(db.String(191), nullable=False)
    description = db.Column(db.Text, nullable=True)

    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    # 3 product images
    image1_url = db.Column(db.String(255), nullable=True)
    image2_url = db.Column(db.String(255), nullable=True)
    image3_url = db.Column(db.String(255), nullable=True)

    # Admin approval status
    status = db.Column(
        db.Enum("PENDING_APPROVAL", "APPROVED", "REJECTED", name="product_status"),
        nullable=False,
        default="PENDING_APPROVAL",
        server_default="PENDING_APPROVAL",
    )

    # Timestamps
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

    # Relationship to farmer (NO backref name here, we already define it on User)
    farmer = db.relationship(
        "User",
        foreign_keys=[farmer_id]
    )

    # 🔴 This is the IMPORTANT line to fix your error:
    # Product.order_items <-> OrderItem.product
    order_items = db.relationship(
        "OrderItem",
        back_populates="product",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Product {self.id} {self.name} ({self.status})>"
