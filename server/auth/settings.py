import settings


DEFAULT_SECRET_KEY = 'aAhf4Wexd#S'

SECRET_KEY = getattr(settings, 'SECRET_KEY', DEFAULT_SECRET_KEY)
