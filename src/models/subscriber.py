import uuid
import hashlib
from datetime import datetime
from app import db


class Subscriber(db.Model):
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=True)
    position = db.Column(db.Integer, nullable=False)
    referral_code = db.Column(db.String(20), unique=True, nullable=False)
    referred_by = db.Column(db.String(20), nullable=True)
    referral_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="waiting")  # waiting, approved, rejected
    confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(64), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    source = db.Column(db.String(100), nullable=True)  # utm_source
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, name=None, referred_by=None, ip_address=None, source=None):
        self.email = email.lower().strip()
        self.name = name
        self.referral_code = self._generate_referral_code(email)
        self.referred_by = referred_by
        self.confirmation_token = str(uuid.uuid4()).replace("-", "")
        self.ip_address = ip_address
        self.source = source
        self.position = Subscriber.query.count() + 1

    def _generate_referral_code(self, email: str) -> str:
        """Generate unique referral code from email."""
        hash_val = hashlib.md5(email.encode()).hexdigest()[:8].upper()
        return f"REF{hash_val}"

    def confirm_email(self):
        self.confirmed = True
        self.confirmed_at = datetime.utcnow()

    def approve(self):
        self.status = "approved"
        self.approved_at = datetime.utcnow()

    @property
    def effective_position(self):
        """Position after referral bonuses."""
        bonus = self.referral_count * 5
        return max(1, self.position - bonus)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "position": self.position,
            "effective_position": self.effective_position,
            "referral_code": self.referral_code,
            "referral_count": self.referral_count,
            "status": self.status,
            "confirmed": self.confirmed,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
        }


class WaitlistSettings(db.Model):
    __tablename__ = "waitlist_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get(cls, key, default=None):
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default

    @classmethod
    def set(cls, key, value):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
