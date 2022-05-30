import os

if os.getenv("ENV") == "production":
    from config.settings.production import *
elif os.getenv("ENV") == "development":
    from config.settings.development import *
else:
    from config.settings.development import *
