from datetime import datetime
from extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("audit_logs", lazy="dynamic"))

    def __repr__(self):
        return f"<AuditLog id={self.id} action={self.action}>"
