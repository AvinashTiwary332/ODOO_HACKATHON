from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import LeaveRequest, db
from utils.helper import current_user, login_required, parse_date


leave_bp = Blueprint("leave", __name__, url_prefix="/leave")


@leave_bp.route("/", methods=["GET", "POST"])
@login_required
def leave_home():
    employee = current_user().employee
    if request.method == "POST":
        try:
            start = parse_date(request.form.get("start_date"), "start date")
            end = parse_date(request.form.get("end_date"), "end date")
            if end < start:
                raise ValueError("End date cannot be before start date.")
            db.session.add(LeaveRequest(employee_id=employee.id, leave_type=request.form["leave_type"], start_date=start, end_date=end, remarks=request.form.get("remarks")))
            db.session.commit()
            flash("Leave request submitted.", "success")
            return redirect(url_for("leave.leave_home"))
        except Exception as exc:
            db.session.rollback()
            flash(str(exc), "danger")
    leaves = LeaveRequest.query.filter_by(employee_id=employee.id).order_by(LeaveRequest.created_at.desc()).all()
    return render_template("leave.html", leaves=leaves)
