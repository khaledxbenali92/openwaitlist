"""
Public Routes — Landing page & signup
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from src.models.subscriber import Subscriber
from src.services.waitlist_service import WaitlistService
from app import db

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    total = Subscriber.query.filter_by(confirmed=True).count()
    return render_template("index.html",
                           app_name=current_app.config["APP_NAME"],
                           app_description=current_app.config["APP_DESCRIPTION"],
                           total_subscribers=total)


@public_bp.route("/join", methods=["POST"])
def join():
    email = request.form.get("email", "").strip()
    name = request.form.get("name", "").strip()
    referral_code = request.form.get("ref", "").strip()

    service = WaitlistService()
    result = service.add_subscriber(
        email=email,
        name=name,
        referred_by=referral_code,
        ip_address=request.remote_addr,
        source=request.args.get("utm_source")
    )

    if result["success"]:
        return redirect(url_for("public.thank_you", token=result["token"]))
    else:
        flash(result["message"], "error")
        return redirect(url_for("public.index"))


@public_bp.route("/confirm/<token>")
def confirm_email(token):
    subscriber = Subscriber.query.filter_by(confirmation_token=token).first()

    if not subscriber:
        flash("Invalid or expired confirmation link.", "error")
        return redirect(url_for("public.index"))

    if subscriber.confirmed:
        flash("Email already confirmed!", "info")
    else:
        subscriber.confirm_email()
        db.session.commit()

        # Credit referrer
        if subscriber.referred_by:
            referrer = Subscriber.query.filter_by(
                referral_code=subscriber.referred_by
            ).first()
            if referrer:
                referrer.referral_count += 1
                db.session.commit()

    return redirect(url_for("public.status", token=token))


@public_bp.route("/status/<token>")
def status(token):
    subscriber = Subscriber.query.filter_by(confirmation_token=token).first_or_404()
    total = Subscriber.query.filter_by(confirmed=True).count()

    return render_template("status.html",
                           subscriber=subscriber,
                           total=total,
                           app_name=current_app.config["APP_NAME"])


@public_bp.route("/thank-you/<token>")
def thank_you(token):
    subscriber = Subscriber.query.filter_by(confirmation_token=token).first_or_404()
    return render_template("thank_you.html",
                           subscriber=subscriber,
                           app_name=current_app.config["APP_NAME"])


@public_bp.route("/unsubscribe/<token>")
def unsubscribe(token):
    subscriber = Subscriber.query.filter_by(confirmation_token=token).first_or_404()
    db.session.delete(subscriber)
    db.session.commit()
    flash("You've been removed from the waitlist.", "info")
    return redirect(url_for("public.index"))
