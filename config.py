import boto3
import os




class Config():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get("SECRET_KEY", "app_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASEDIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_PORT = os.environ.get("port", 5000)
    S3_BUCKET = "l-founders-storage"

    S3_KEY = os.environ.get("aws_access_key")
    S3_SECRET = os.environ.get("aws_secret_key")
    REGION = os.environ.get("aws_region", "sa-east-1")
