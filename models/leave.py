from .user import TimestampMixin, db


class LeaveRequest(db.Model, TimestampMixin):
    __tablename__ = "leave_requests"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    leave_type = db.Column(db.String(40), nullable=False)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=False)
    remarks = db.Column(db.Text)
    status = db.Column(db.String(30), default="Pending", nullable=False, index=True)
    admin_comments = db.Column(db.Text)

    employee = db.relationship("Employee", back_populates="leave_requests")

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1
