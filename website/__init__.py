from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Create SQLAlchemy instance
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth
    from .weight_tracker import weight_tracker_bp  # Import the weight tracker blueprint

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(weight_tracker_bp, url_prefix='/weight')  # Register the weight tracker blueprint

    # Import models
    from .models import User, Note, QuestionnaireResponse, WeightEntry
    
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define the user loader function
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Inject current_user into templates
    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return dict(user=current_user)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
