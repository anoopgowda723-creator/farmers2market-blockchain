# models/notification.py
from extensions import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.BigInteger, primary_key=True)

    # IMPORTANT: this MUST have a ForeignKey to users.id
    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=True)
    is_read = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    # relationship back to user
    user = db.relationship(
        "User",
        back_populates="notifications",
    )
