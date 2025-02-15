# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://blendirrustemi@localhost:5432/vikings')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
