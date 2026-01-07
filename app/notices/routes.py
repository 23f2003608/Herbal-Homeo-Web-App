# app/testimonials/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from sqlalchemy import func
from datetime import datetime
import os
from ..models import db, Notice

notices_bp = Blueprint("notices", __name__, url_prefix="/noticeboard")

@notices_bp.route("/manage", methods=["GET", "POST"])
@login_required
def manage_notices():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        category = request.form.get("category")
        
        new_notice = Notice(title=title, content=content, category=category)
        db.session.add(new_notice)
        db.session.commit()
        flash("Notice published to homepage!", "success")
        return redirect(url_for('notices.manage_notices'))

    all_notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template("notices/manage.html", notices=all_notices)

@notices_bp.route("/delete/<int:id>")
@login_required
def delete_notice(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    flash("Notice removed.", "info")
    return redirect(url_for('notices.manage_notices'))