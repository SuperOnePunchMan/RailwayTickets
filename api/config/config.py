import os
from decouple import config
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

class Config():
    SECRET_KEY = config("SECRET_KEY", "secret")
    DEBUG= True
    SQLALCHEMY_TRACK_MODIFICATION= False
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(minutes= 1000)
    JWT_REFRESH_TOKEN= EXPIRES = timedelta(days=7)
    JWT_SECRET_KEY= config("JWT_SECRET_KEY")

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI= config("DATABASE_URI")
    SQLALCHEMY_ECHO = True

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict ={
    "dev":DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}