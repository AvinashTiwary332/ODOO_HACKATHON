from .user import TimestampMixin, db


class Payroll(db.Model, TimestampMixin):
    __tablename__ = "payroll"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    month = db.Column(db.String(20), nullable=False, index=True)
    base_salary = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    bonus = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    deductions = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    net_salary = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    status = db.Column(db.String(30), default="Generated", nullable=False)

    employee = db.relationship("Employee", back_populates="payrolls")

    def recalculate(self):
        self.net_salary = float(self.base_salary or 0) + float(self.bonus or 0) - float(self.deductions or 0)
