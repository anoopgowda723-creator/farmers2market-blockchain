# backend/models/user.py

from datetime import datetime
from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(
        db.BigInteger,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    phone = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.Enum(
            "BUYER",
            "FARMER",
            "DELIVERY",
            "ADMIN",
            name="user_role"
        ),
        nullable=False
    )

    wallet_address = db.Column(
        db.String(100),
        nullable=True
    )

    is_approved = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


    # Farmer warehouse location

    warehouse_lat = db.Column(
        db.Numeric(10, 6),
        nullable=True
    )

    warehouse_lng = db.Column(
        db.Numeric(10, 6),
        nullable=True
    )


    # Bank details

    bank_account_no = db.Column(
        db.String(32),
        nullable=True
    )

    ifsc_code = db.Column(
        db.String(20),
        nullable=True
    )

    upi_id = db.Column(
        db.String(100),
        nullable=True
    )


    # =====================================
    # Relationships
    # =====================================


    # Farmer products

    products = db.relationship(
        "Product",
        back_populates="farmer",
        lazy="dynamic"
    )


    # Buyer orders

    orders_as_buyer = db.relationship(
        "Order",
        foreign_keys="Order.buyer_id",
        back_populates="buyer",
        lazy="dynamic",
        overlaps="buyer_orders"
    )


    # Farmer orders

    orders_as_farmer = db.relationship(
        "Order",
        foreign_keys="Order.farmer_id",
        back_populates="farmer",
        lazy="dynamic",
        overlaps="farmer_orders"
    )


    # Delivery partner orders

    deliveries = db.relationship(
        "Delivery",
        back_populates="delivery_partner",
        lazy="dynamic"
    )


    # Notifications

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        lazy="dynamic"
    )


    # =====================================
    # String Representation
    # =====================================

    def __repr__(self):

        return (
            f"<User {self.id} "
            f"{self.email} "
            f"({self.role})>"
        )