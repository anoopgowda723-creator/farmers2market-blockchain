from datetime import datetime
from extensions import db


class Dispute(db.Model):
    __tablename__ = "disputes"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False)
    raised_by_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum(
            "OPEN",
            "IN_REVIEW",
            "RESOLVED_BUYER",
            "RESOLVED_FARMER",
            "REFUNDED",
            "REJECTED",
            name="dispute_status",
        ),
        nullable=False,
        default="OPEN",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = db.relationship("Order", back_populates="disputes")
    raised_by = db.relationship("User", backref=db.backref("disputes_raised", lazy="dynamic"))

    def __repr__(self):
        return f"<Dispute order={self.order_id} status={self.status}>"
