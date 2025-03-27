import secrets
from datetime import datetime, timedelta

def generate_token():
    return secrets.token_urlsafe(32)

def get_token_expiry(hours=1):
    return datetime.now() + timedelta(hours=hours)

def is_token_valid(expiry_date):
    return datetime.now() < expiry_date