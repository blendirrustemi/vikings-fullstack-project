# app/utils/app_context.py
from app import create_app

def get_app_context():
    app = create_app()
    return app.app_context()
