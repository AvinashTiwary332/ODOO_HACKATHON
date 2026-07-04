from datetime import date, datetime
from .user import TimestampMixin, db


class Attendance(db.Model, TimestampMixin):
    __tablename__ = "attendance"
    __table_args__ = (db.UniqueConstraint("employee_id", "date", name="uq_employee_attendance_date"),)

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    status = db.Column(db.String(30), default="Present", nullable=False, index=True)
    approved = db.Column(db.Boolean, default=False, nullable=False)

    employee = db.relationship("Employee", back_populates="attendance_records")

    @property
    def working_hours(self):
        if self.check_in and self.check_out:
            return round((self.check_out - self.check_in).total_seconds() / 3600, 2)
        return 0

    def checkout_now(self):
        self.check_out = datetime.utcnow()
        hours = self.working_hours
        self.status = "Half Day" if hours and hours < 4 else "Present"
