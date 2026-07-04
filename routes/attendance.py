from datetime import date, datetime
from flask import Blueprint, flash, redirect, render_template, url_for
from models import Attendance, db
from utils.helper import current_user, login_required


attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")


@attendance_bp.route("/")
@login_required
def history():
    employee = current_user().employee
    records = Attendance.query.filter_by(employee_id=employee.id).order_by(Attendance.date.desc()).all()
    today_record = Attendance.query.filter_by(employee_id=employee.id, date=date.today()).first()
    return render_template("attendance.html", records=records, today_record=today_record, admin_view=False)


@attendance_bp.route("/check-in", methods=["POST"])
@login_required
def check_in():
    employee = current_user().employee
    record = Attendance.query.filter_by(employee_id=employee.id, date=date.today()).first()
    if record:
        flash("You have already checked in today.", "warning")
    else:
        db.session.add(Attendance(employee_id=employee.id, check_in=datetime.utcnow(), status="Present"))
        db.session.commit()
        flash("Checked in successfully.", "success")
    return redirect(url_for("attendance.history"))


@attendance_bp.route("/check-out", methods=["POST"])
@login_required
def check_out():
    employee = current_user().employee
    record = Attendance.query.filter_by(employee_id=employee.id, date=date.today()).first()
    if not record:
        flash("Please check in first.", "warning")
    elif record.check_out:
        flash("You have already checked out today.", "warning")
    else:
        record.checkout_now()
        db.session.commit()
        flash("Checked out successfully.", "success")
    return redirect(url_for("attendance.history"))
