"""
API Routes — REST API for embed widget
"""

from flask import Blueprint, request, jsonify, current_app
from src.models.subscriber import Subscriber
from src.services.waitlist_service import WaitlistService

api_bp = Blueprint("api", __name__)


@api_bp.route("/join", methods=["POST"])
def api_join():
    """API endpoint for embedded widget."""
    data = request.get_json() or request.form
    email = data.get("email", "").strip()
    name = data.get("name", "").strip()
    ref = data.get("ref", "").strip()

    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400

    service = WaitlistService()
    result = service.add_subscriber(
        email=email, name=name, referred_by=ref,
        ip_address=request.remote_addr,
        source=data.get("source")
    )

    return jsonify(result), 200 if result["success"] else 400


@api_bp.route("/stats", methods=["GET"])
def api_stats():
    """Public stats endpoint."""
    total = Subscriber.query.filter_by(confirmed=True).count()
    return jsonify({
        "total_subscribers": total,
        "app_name": current_app.config["APP_NAME"],
    })


@api_bp.route("/position/<token>", methods=["GET"])
def api_position(token):
    """Get subscriber position."""
    subscriber = Subscriber.query.filter_by(confirmation_token=token).first()
    if not subscriber:
        return jsonify({"success": False, "message": "Not found"}), 404

    return jsonify({
        "success": True,
        "position": subscriber.effective_position,
        "referral_code": subscriber.referral_code,
        "referral_count": subscriber.referral_count,
    })
