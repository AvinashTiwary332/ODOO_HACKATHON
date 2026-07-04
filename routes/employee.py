import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from models import Employee, Notification, db
from utils.helper import current_user, login_required


employee_bp = Blueprint("employee", __name__, url_prefix="/employee")


@employee_bp.route("/dashboard")
@login_required
def dashboard():
    employee = current_user().employee
    notifications = Notification.query.filter_by(user_id=current_user().id).order_by(Notification.created_at.desc()).limit(6).all()
    return render_template("dashboard.html", employee=employee, notifications=notifications)


@employee_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    employee = current_user().employee
    if request.method == "POST":
        employee.phone = request.form.get("phone")
        employee.address = request.form.get("address")
        image = request.files.get("profile_image")
        if image and image.filename:
            filename = secure_filename(f"{employee.employee_id}_{image.filename}")
            image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            employee.profile_image = filename
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("employee.profile"))
    return render_template("profile.html", employee=employee, editable=False)
