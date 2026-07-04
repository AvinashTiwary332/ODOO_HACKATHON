from flask import Flask, render_template
from config import Config
from models import db
from routes import admin_bp, attendance_bp, auth_bp, employee_bp, leave_bp, payroll_bp
from utils.helper import current_user, seed_demo_data


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(payroll_bp)

    @app.context_processor
    def inject_user():
        return {"current_user": current_user()}

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("error.html", code=403, title="Access denied", message="You do not have permission to open this page."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", code=404, title="Page not found", message="The page you requested does not exist."), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("error.html", code=500, title="Server error", message="Something went wrong. Please try again."), 500

    with app.app_context():
        db.create_all()
        seed_demo_data()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
