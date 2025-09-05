import os
from dataclasses import dataclass


@dataclass
class Settings:
    flask_secret: str = os.getenv("FLASK_SECRET", "dev-secret")
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/contesthub")
    client_origin: str = os.getenv("CLIENT_ORIGIN", "http://localhost:3000")
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "974236313972-ihe5fnhms71lv4u840q790i03guis8t4.apps.googleusercontent.com")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "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")
    google_redirect_uri: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/api/auth/google/callback")
    sendgrid_api_key: str = os.getenv("SENDGRID_API_KEY", "")


settings = Settings()


