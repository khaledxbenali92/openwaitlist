"""
Admin Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from src.models.subscriber import Subscriber
from src.services.email_service import EmailService
from app import db

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == current_app.config["ADMIN_PASSWORD"]:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))
    return render_template("admin_login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("public.index"))


@admin_bp.route("/")
@admin_required
def dashboard():
    page = request.args.get("page", 1, type=int)
    status_filter = request.args.get("status", "all")
    search = request.args.get("search", "")

    query = Subscriber.query
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    if search:
        query = query.filter(Subscriber.email.contains(search))

    subscribers = query.order_by(Subscriber.position).paginate(
        page=page, per_page=50, error_out=False
    )

    stats = {
        "total": Subscriber.query.count(),
        "confirmed": Subscriber.query.filter_by(confirmed=True).count(),
        "approved": Subscriber.query.filter_by(status="approved").count(),
        "waiting": Subscriber.query.filter_by(status="waiting").count(),
    }

    return render_template("admin_dashboard.html",
                           subscribers=subscribers,
                           stats=stats,
                           status_filter=status_filter,
                           search=search)


@admin_bp.route("/approve/<int:sub_id>", methods=["POST"])
@admin_required
def approve(sub_id):
    subscriber = Subscriber.query.get_or_404(sub_id)
    subscriber.approve()
    db.session.commit()

    email_service = EmailService()
    email_service.send_approval(subscriber)

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/export")
@admin_required
def export_csv():
    import csv
    import io
    from flask import Response

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Email", "Name", "Position", "Referrals", "Status", "Confirmed", "Joined"])

    for sub in Subscriber.query.order_by(Subscriber.position).all():
        writer.writerow([
            sub.id, sub.email, sub.name or "", sub.position,
            sub.referral_count, sub.status,
            "Yes" if sub.confirmed else "No",
            sub.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=waitlist.csv"}
    )


@admin_bp.route("/blast", methods=["POST"])
@admin_required
def email_blast():
    """Send email to all confirmed subscribers."""
    subject = request.form.get("subject")
    body = request.form.get("body")

    subscribers = Subscriber.query.filter_by(confirmed=True).all()
    email_service = EmailService()

    sent = 0
    for sub in subscribers:
        try:
            email_service.send_custom(sub, subject, body)
            sent += 1
        except Exception:
            pass

    return redirect(url_for("admin.dashboard"))
