from .user import TimestampMixin, db


class Employee(db.Model, TimestampMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = db.Column(db.String(40), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(30))
    address = db.Column(db.Text)
    salary = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    profile_image = db.Column(db.String(255), default="default-avatar.svg")
    documents = db.Column(db.Text)

    user = db.relationship("User", back_populates="employee")
    attendance_records = db.relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    leave_requests = db.relationship("LeaveRequest", back_populates="employee", cascade="all, delete-orphan")
    payrolls = db.relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")
