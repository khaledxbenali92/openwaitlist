"""
Configuration
"""

import os
from datetime import timedelta


class Config:
    # Core
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///waitlist.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@example.com")

    # Waitlist Settings
    APP_NAME = os.getenv("APP_NAME", "My App")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Something amazing is coming.")
    REFERRAL_REWARD = int(os.getenv("REFERRAL_REWARD", 5))
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
