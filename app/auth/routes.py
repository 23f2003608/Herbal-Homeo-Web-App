# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from ..models import Doctor

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Support both PIN and username/password auth
        pin = request.form.get("pin")
        username = request.form.get("username")
        password = request.form.get("password")

        # PIN-based authentication (from index.html modal)
        if pin:
            if pin == "2023":  # Clinic PIN
                # Get or create default doctor account
                doctor = Doctor.query.filter_by(username="dr_shikhar").first()
                if not doctor:
                    # Create default doctor if doesn't exist
                    doctor = Doctor(username="dr_shikhar", full_name="Dr. Shikhar Sharma")
                    doctor.set_password("default2023")
                    from .. import db
                    db.session.add(doctor)
                    db.session.commit()
                login_user(doctor)
                # Return JSON response for AJAX request
                return {"status": "success", "message": "Logged in successfully"}, 200
            else:
                return {"status": "error", "message": "Invalid PIN"}, 401
        # Username/password authentication (from dedicated login page)
        elif username and password:
            doctor = Doctor.query.filter_by(username=username).first()
            if doctor and check_password_hash(doctor.password_hash, password):
                login_user(doctor)
                return redirect(url_for("dashboard.doctor_dashboard"))
            return {"status": "error", "message": "Invalid credentials"}, 401
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
