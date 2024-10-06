from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '4b4d81f7ef1fd0e05b738dbe9cd924f5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_BINDS'] = {
        'database1': 'sqlite:///site.db',
        'database2': 'sqlite:///site2.db'
    }

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register your blueprints/routes here
    from Ignosis.routes import your_blueprint
    app.register_blueprint(your_blueprint)

    return app, db, bcrypt, login_manager

app, db, bcrypt, login_manager = create_app()