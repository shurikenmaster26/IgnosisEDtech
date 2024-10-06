from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b4d81f7ef1fd0e05b738dbe9cd924f5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_BINDS'] = {
    'database1': 'sqlite:///site.db',
    'database2': 'sqlite:///site2.db'
}

# Initialize components
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import and register your blueprints/routes here to avoid circular import
from Ignosis.routes import create_routes

create_routes(app)