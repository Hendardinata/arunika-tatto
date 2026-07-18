from flask import Flask
from backend.app.config.settings import config_by_name
from backend.app.database.connection import mongo
from backend.app.utils.logger import setup_logger
from backend.app.exceptions.error_handlers import register_error_handlers
import os

def create_app(config_name="dev"):
    app = Flask(__name__, 
                template_folder=os.path.abspath('frontend/templates'),
                static_folder=os.path.abspath('frontend/static'))
                
    app.config.from_object(config_by_name[config_name])
    
    # Init Database
    mongo.init_app(app)
    
    # Setup Logger
    setup_logger(app)
    
    # Register Error Handlers
    register_error_handlers(app)
    
    # Register Blueprints
    from backend.app.controllers.auth_controller import auth_bp
    from backend.app.controllers.public_controller import public_bp
    from backend.app.controllers.customer_controller import customer_bp
    from backend.app.controllers.admin_controller import admin_bp
    from backend.app.controllers.api_controller import api_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    # Context Processor for Templates
    from datetime import datetime
    from flask import session
    @app.context_processor
    def inject_globals():
        doc = mongo.db.settings.find_one({"key": "studio"}) or {}
        return {
            "now": datetime.now(),
            "session": session,
            "studio_settings": doc
        }
        
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
