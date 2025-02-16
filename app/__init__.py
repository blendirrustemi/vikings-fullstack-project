# app/__init__.py
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from app.db import db 
from app.utils.database import store_characters

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()  # This will create the tables if they do not exist
        db.session.commit()
        
    """
    Scheduler that calls the store_characters function every 24 hours.
    """
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(func=store_characters, trigger='interval', hours=24)  # Every 24 hours

    from app.routes.api import api_bp
    from app.routes.views import views_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(views_bp)

    # shutdown the scheduler on app exit
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if scheduler.running:
            scheduler.shutdown()

    return app