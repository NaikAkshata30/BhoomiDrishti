import os
from flask import Flask
from flask_cors import CORS
from config import get_config
from database import init_db
from services.prediction_service import initialize_prediction_service

def create_app(config=None):
    """
    Application factory function.
    Creates and configures a Flask application instance.
    
    Args:
        config: Configuration class to use. If None, uses environment-based config.
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Initialize ML prediction service
    initialize_prediction_service(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints (routes)
    from route import project_routes, map_routes, dashboard_routes, prediction_routes, data_quality_routes, auth_routes
    app.register_blueprint(project_routes.bp)
    app.register_blueprint(map_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    app.register_blueprint(prediction_routes.bp)
    app.register_blueprint(data_quality_routes.bp)
    app.register_blueprint(auth_routes.bp)
    with app.app_context():
        auth_routes.seed_official_accounts()
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'Server is running'}, 200
    
    return app


def register_error_handlers(app):
    """
    Register global error handlers for the application.
    
    Args:
        app: Flask application instance
    """
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Not found',
            'status': 404
        }, 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return {
            'error': 'Bad request',
            'status': 400
        }, 400
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'error': 'Internal server error',
            'status': 500
        }, 500


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
