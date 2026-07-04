from .admin import admin_bp
from .attendance import attendance_bp
from .auth import auth_bp
from .employee import employee_bp
from .leave import leave_bp
from .payroll import payroll_bp

__all__ = ["admin_bp", "attendance_bp", "auth_bp", "employee_bp", "leave_bp", "payroll_bp"]
