"""
Email Service
"""

from flask import render_template_string, current_app, url_for
from flask_mail import Message
from app import mail


CONFIRMATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:20px;background:#f9fafb">
<div style="background:white;border-radius:12px;padding:32px;border:1px solid #e5e7eb">
  <h1 style="color:#1b2a4a;font-size:1.5rem">🚀 You're on the list!</h1>
  <p style="color:#4b5563">Hi {{ name or 'there' }},</p>
  <p style="color:#4b5563">Thanks for joining the <strong>{{ app_name }}</strong> waitlist.
  Please confirm your email to secure your spot.</p>
  <div style="text-align:center;margin:28px 0">
    <a href="{{ confirm_url }}" style="background:#0d7377;color:white;padding:14px 28px;
       border-radius:8px;text-decoration:none;font-weight:bold;font-size:1rem">
      ✅ Confirm My Email
    </a>
  </div>
  <p style="color:#6b7280;font-size:0.9rem">Your position: <strong>#{{ position }}</strong></p>
  <hr style="border:none;border-top:1px solid #e5e7eb;margin:20px 0">
  <p style="color:#6b7280;font-size:0.85rem">
    Share your referral link to move up the list:<br>
    <strong>{{ referral_url }}</strong>
  </p>
  <p style="color:#9ca3af;font-size:0.75rem;margin-top:20px">
    Don't want to be on the list?
    <a href="{{ unsubscribe_url }}" style="color:#9ca3af">Unsubscribe</a>
  </p>
</div>
</body>
</html>
"""

APPROVAL_TEMPLATE = """
<!DOCTYPE html>
<html>
<body style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:20px">
<div style="background:white;border-radius:12px;padding:32px;border:1px solid #e5e7eb">
  <h1 style="color:#1b2a4a">🎉 You're in!</h1>
  <p>Hi {{ name or 'there' }},</p>
  <p>Great news — you've been approved for <strong>{{ app_name }}</strong>!</p>
  <div style="text-align:center;margin:28px 0">
    <a href="{{ app_url }}" style="background:#0d7377;color:white;padding:14px 28px;
       border-radius:8px;text-decoration:none;font-weight:bold">
      🚀 Get Started Now
    </a>
  </div>
</div>
</body>
</html>
"""


class EmailService:

    def send_confirmation(self, subscriber):
        with current_app.app_context():
            confirm_url = url_for(
                "public.confirm_email",
                token=subscriber.confirmation_token,
                _external=True
            )
            referral_url = url_for(
                "public.index",
                ref=subscriber.referral_code,
                _external=True
            )
            unsubscribe_url = url_for(
                "public.unsubscribe",
                token=subscriber.confirmation_token,
                _external=True
            )

            html = render_template_string(CONFIRMATION_TEMPLATE,
                name=subscriber.name,
                app_name=current_app.config["APP_NAME"],
                confirm_url=confirm_url,
                position=subscriber.position,
                referral_url=referral_url,
                unsubscribe_url=unsubscribe_url
            )

            msg = Message(
                subject=f"Confirm your spot on the {current_app.config['APP_NAME']} waitlist",
                recipients=[subscriber.email],
                html=html
            )
            mail.send(msg)

    def send_approval(self, subscriber):
        with current_app.app_context():
            html = render_template_string(APPROVAL_TEMPLATE,
                name=subscriber.name,
                app_name=current_app.config["APP_NAME"],
                app_url=url_for("public.index", _external=True)
            )
            msg = Message(
                subject=f"🎉 You're approved for {current_app.config['APP_NAME']}!",
                recipients=[subscriber.email],
                html=html
            )
            mail.send(msg)

    def send_custom(self, subscriber, subject, body):
        msg = Message(subject=subject, recipients=[subscriber.email], html=body)
        mail.send(msg)
