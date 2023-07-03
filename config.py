import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Your SECRET KEY"

ADMIN_USERNAME = 'Username'
ADMIN_PASSWORD = 'Password'

print(Config.SECRET_KEY)
