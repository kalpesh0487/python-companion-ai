from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import db
from routes.companion import companion_bp
from routes.chat import chat_bp
from routes.category import category_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(companion_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(category_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()

    # Create database tables
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create tables with new schema

        # Create initial categories
        from models import Category
        categories = [
            Category(name="Scientists"),
            Category(name="Philosophers"),
            Category(name="Artists"),
            Category(name="Leaders"),
            Category(name="Innovators")
        ]
        db.session.add_all(categories)
        db.session.commit()

    app.run(debug=True, host='0.0.0.0', port=5000)