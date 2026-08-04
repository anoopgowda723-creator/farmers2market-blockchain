import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Flask
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )


    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Razorpay
    RAZORPAY_KEY_ID = os.getenv(
        "RAZORPAY_KEY_ID"
    )

    RAZORPAY_KEY_SECRET = os.getenv(
        "RAZORPAY_KEY_SECRET"
    )


    # Google Maps
    GOOGLE_MAPS_API_KEY = os.getenv(
        "GOOGLE_MAPS_API_KEY"
    )


    # Blockchain
    WEB3_PROVIDER_URI = os.getenv(
        "WEB3_PROVIDER_URI"
    )

    SMART_CONTRACT_ADDRESS = os.getenv(
        "SMART_CONTRACT_ADDRESS"
    )

    SMART_CONTRACT_ABI_PATH = os.getenv(
        "SMART_CONTRACT_ABI_PATH"
    )

    SYSTEM_WALLET_ADDRESS = os.getenv(
        "SYSTEM_WALLET_ADDRESS"
    )

    SYSTEM_WALLET_PRIVATE_KEY = os.getenv(
        "SYSTEM_WALLET_PRIVATE_KEY"
    )


    # Email
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    EMAIL_HOST_USER = os.getenv(
        "EMAIL_HOST_USER"
    )

    EMAIL_HOST_PASSWORD = os.getenv(
        "EMAIL_HOST_PASSWORD"
    )


    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv(
        "TWILIO_ACCOUNT_SID"
    )

    TWILIO_AUTH_TOKEN = os.getenv(
        "TWILIO_AUTH_TOKEN"
    )

    TWILIO_FROM_NUMBER = os.getenv(
        "TWILIO_FROM_NUMBER"
    )



class DevelopmentConfig(Config):
    DEBUG = True



class ProductionConfig(Config):
    DEBUG = False