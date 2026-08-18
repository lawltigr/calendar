from flask import Flask
from flask_wtf import CSRFProtect
from config import Config
from extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to open this page."
    login_manager.login_message_category = "info"
    CSRFProtect(app)

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from routes.auth import auth_bp
    from routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    with app.app_context():
        db.create_all()
    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)