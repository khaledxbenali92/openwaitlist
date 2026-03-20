"""
Waitlist Service — Core business logic
"""

from src.models.subscriber import Subscriber
from src.services.email_service import EmailService
from app import db


class WaitlistService:

    def add_subscriber(self, email: str, name: str = None,
                       referred_by: str = None, ip_address: str = None,
                       source: str = None) -> dict:
        """Add a new subscriber to the waitlist."""

        if not email or "@" not in email:
            return {"success": False, "message": "Please enter a valid email address."}

        # Check duplicate
        existing = Subscriber.query.filter_by(email=email.lower().strip()).first()
        if existing:
            return {
                "success": False,
                "message": "You're already on the waitlist!",
                "token": existing.confirmation_token
            }

        # Validate referral code
        referrer = None
        if referred_by:
            referrer = Subscriber.query.filter_by(referral_code=referred_by).first()
            if not referrer:
                referred_by = None

        # Create subscriber
        subscriber = Subscriber(
            email=email,
            name=name,
            referred_by=referred_by,
            ip_address=ip_address,
            source=source
        )
        db.session.add(subscriber)
        db.session.commit()

        # Send confirmation email
        try:
            email_service = EmailService()
            email_service.send_confirmation(subscriber)
        except Exception:
            pass  # Don't fail if email fails

        return {
            "success": True,
            "message": "You're on the waitlist! Check your email to confirm.",
            "position": subscriber.position,
            "token": subscriber.confirmation_token,
            "referral_code": subscriber.referral_code,
        }

    def get_stats(self) -> dict:
        return {
            "total": Subscriber.query.count(),
            "confirmed": Subscriber.query.filter_by(confirmed=True).count(),
            "approved": Subscriber.query.filter_by(status="approved").count(),
        }
