from datetime import datetime
from extensions import db


class OtpLog(db.Model):
    __tablename__ = "otp_logs"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    channel = db.Column(
        db.Enum("SMS", "EMAIL", name="otp_channel"),
        nullable=False,
        default="EMAIL",
    )
    otp_code = db.Column(db.String(10), nullable=False)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("otp_logs", lazy="dynamic"))

    def __repr__(self):
        return f"<OtpLog user={self.user_id} channel={self.channel} used={self.is_used}>"
