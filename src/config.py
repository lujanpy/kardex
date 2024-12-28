from decouple import config


class Config:
    SECRET_KEY = config('SECRET_KEY', default='default_secret_key')


class Develomenptconfig(Config):
    DEBUG = True


config = {
    'develoment': Develomenptconfig
}
