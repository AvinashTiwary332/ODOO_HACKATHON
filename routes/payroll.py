from flask import Blueprint, render_template
from models import Payroll
from utils.helper import current_user, login_required


payroll_bp = Blueprint("payroll", __name__, url_prefix="/payroll")


@payroll_bp.route("/")
@login_required
def payroll_home():
    employee = current_user().employee
    payrolls = Payroll.query.filter_by(employee_id=employee.id).order_by(Payroll.created_at.desc()).all()
    return render_template("payroll.html", payrolls=payrolls, admin_view=False)
