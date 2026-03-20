"""
🚀 OpenWaitlist — Open Source Waitlist Tool
Main Flask Application
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from src.config import Config

db = SQLAlchemy()
mail = Mail()


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    app.config.from_object(Config)
    if config:
        app.config.update(config)

    # Init extensions
    db.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from src.routes.public import public_bp
    from src.routes.api import api_bp
    from src.routes.admin import admin_bp
    from src.routes.dashboard import dashboard_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
