from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    # Create the actual app
    app = Flask(__name__)
    app.config.from_object(config_class)

    Bootstrap(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from models import User

    @login_manager.user_loader
    def load_user(user_id) -> User:
        return User.query.get(user_id)

    # All the routes being imported then registered
    from errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from main import bp as main_bp
    app.register_blueprint(main_bp)

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app


if __name__ == '__main__':
    application = create_app()
