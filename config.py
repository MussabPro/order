import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "nabfiyeghh978r1y989(&Y*&%#V^&%fgegqw)724637567y86R^E@R^R6"

ADMIN_USERNAME = 'Mussab'
ADMIN_PASSWORD = '131416'

print(Config.SECRET_KEY)