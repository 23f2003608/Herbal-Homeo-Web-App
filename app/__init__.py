# app/__init__.py
import os
import socket
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from .models import db, Doctor
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("10.255.255.255", 1))
        return sock.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        sock.close()

@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app_host = os.environ.get("HOST", os.environ.get("FLASK_RUN_HOST", "0.0.0.0"))
    app_port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 3000)))

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", SECRET_KEY),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", SQLALCHEMY_DATABASE_URI),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER", UPLOAD_FOLDER),
        APP_HOST=app_host,
        APP_PORT=app_port
    )

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Enable CORS with credentials support
    CORS(app, supports_credentials=True)

    db.init_app(app)
    login_manager.init_app(app)

    @app.context_processor
    def inject_network_info():
        local_ip = get_local_ip()
        local_url = f"http://127.0.0.1:{app.config['APP_PORT']}"
        network_url = None
        if local_ip and local_ip != "127.0.0.1":
            network_url = f"http://{local_ip}:{app.config['APP_PORT']}"
        return {
            "network_url": network_url,
            "local_url": local_url
        }

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
