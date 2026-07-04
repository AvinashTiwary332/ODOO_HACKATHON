from datetime import date
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import func
from models import Attendance, Employee, LeaveRequest, Payroll, User, db
from utils.helper import login_required, notify, parse_date, roles_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@roles_required("Admin", "HR Officer")
def dashboard():
    today = date.today()
    stats = {
        "employees": Employee.query.count(),
        "present": Attendance.query.filter_by(date=today, status="Present").count(),
        "absent": max(Employee.query.count() - Attendance.query.filter_by(date=today).count(), 0),
        "pending": LeaveRequest.query.filter_by(status="Pending").count(),
        "approved": LeaveRequest.query.filter_by(status="Approved").count(),
        "rejected": LeaveRequest.query.filter_by(status="Rejected").count(),
        "payroll": db.session.query(func.coalesce(func.sum(Payroll.net_salary), 0)).scalar(),
    }
    recent_leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).limit(6).all()
    return render_template("dashboard.html", stats=stats, recent_leaves=recent_leaves)


@admin_bp.route("/employees")
@login_required
@roles_required("Admin", "HR Officer")
def employee_list():
    q = request.args.get("q", "").strip()
    query = Employee.query.join(User)
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like), Employee.employee_id.ilike(like), Employee.department.ilike(like)))
    return render_template("employee_list.html", employees=query.order_by(Employee.created_at.desc()).all(), q=q)


@admin_bp.route("/employees/<int:employee_id>", methods=["GET", "POST"])
@login_required
@roles_required("Admin", "HR Officer")
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == "POST":
        employee.user.name = request.form["name"].strip()
        employee.department = request.form["department"].strip()
        employee.designation = request.form["designation"].strip()
        employee.phone = request.form.get("phone")
        employee.address = request.form.get("address")
        employee.salary = float(request.form.get("salary") or 0)
        db.session.commit()
        flash("Employee profile updated.", "success")
        return redirect(url_for("admin.employee_list"))
    return render_template("profile.html", employee=employee, editable=True)


@admin_bp.route("/employees/<int:employee_id>/delete", methods=["POST"])
@login_required
@roles_required("Admin")
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee.user)
    db.session.commit()
    flash("Employee deleted.", "info")
    return redirect(url_for("admin.employee_list"))


@admin_bp.route("/approvals", methods=["GET", "POST"])
@login_required
@roles_required("Admin", "HR Officer")
def approvals():
    if request.method == "POST":
        leave = LeaveRequest.query.get_or_404(request.form.get("leave_id"))
        leave.status = request.form.get("action", "Pending")
        leave.admin_comments = request.form.get("comments", "")
        notify(leave.employee.user_id, "Leave status updated", f"Your leave request is now {leave.status}.")
        db.session.commit()
        flash("Leave request updated.", "success")
        return redirect(url_for("admin.approvals"))
    leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
    return render_template("approvals.html", leaves=leaves)


@admin_bp.route("/attendance")
@login_required
@roles_required("Admin", "HR Officer")
def attendance_admin():
    records = Attendance.query.order_by(Attendance.date.desc(), Attendance.created_at.desc()).limit(200).all()
    return render_template("attendance.html", records=records, admin_view=True)


@admin_bp.route("/attendance/<int:record_id>/approve", methods=["POST"])
@login_required
@roles_required("Admin", "HR Officer")
def approve_attendance(record_id):
    record = Attendance.query.get_or_404(record_id)
    record.approved = True
    db.session.commit()
    flash("Attendance approved.", "success")
    return redirect(url_for("admin.attendance_admin"))


@admin_bp.route("/payroll", methods=["GET", "POST"])
@login_required
@roles_required("Admin", "HR Officer")
def payroll():
    if request.method == "POST":
        employee = Employee.query.get_or_404(request.form.get("employee_id"))
        payroll = Payroll(employee_id=employee.id, month=request.form["month"], base_salary=float(request.form.get("base_salary") or employee.salary), bonus=float(request.form.get("bonus") or 0), deductions=float(request.form.get("deductions") or 0))
        payroll.recalculate()
        db.session.add(payroll)
        db.session.commit()
        flash("Payroll generated.", "success")
        return redirect(url_for("admin.payroll"))
    return render_template("payroll.html", payrolls=Payroll.query.order_by(Payroll.created_at.desc()).all(), employees=Employee.query.all(), admin_view=True)
