from datetime import datetime
from extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    notification_type = db.Column(
        db.Enum("EMAIL", "SMS", "PUSH", name="notification_type"),
        nullable=False,
    )
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum("PENDING", "SENT", "FAILED", name="notification_status"),
        nullable=False,
        default="PENDING",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sent_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification user={self.user_id} type={self.notification_type} status={self.status}>"
