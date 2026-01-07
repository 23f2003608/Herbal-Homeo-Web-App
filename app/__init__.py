# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from .models import db, Doctor

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="change-this",
        SQLALCHEMY_DATABASE_URI="sqlite:///herbal_homeo.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER="app/static/uploads"
    )

    # Enable CORS with credentials support
    CORS(app, supports_credentials=True)

    db.init_app(app)
    login_manager.init_app(app)

    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .patients.routes import patients_bp
    from .expenses.routes import expenses_bp
    from .notices.routes import notices_bp
    
    app.register_blueprint(notices_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(expenses_bp)

    @app.route("/")
    def home():
        from flask import render_template
        from .models import Notice # Import the new model
        
        # Fetch the latest 4 active notices to display on the board
        active_notices = Notice.query.filter_by(is_active=True)\
                                     .order_by(Notice.created_at.desc())\
                                     .limit(4).all()
                                     
        return render_template("index.html", active_notices=active_notices)
    with app.app_context():
        db.create_all()

    return app
