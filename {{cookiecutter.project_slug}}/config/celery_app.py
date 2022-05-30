from celery import Celery
# import sentry_sdk
# from sentry_sdk.integrations.celery import CeleryIntegration
from config.settings import settings, get_app

# get_app()

# sentry_sdk.init(
#     dsn='https://examplePublicKey@o0.ingest.sentry.io/0',
#     integrations=[CeleryIntegration()]
# )

celery_app = Celery(f'{settings.PROJECT_NAME}-worker',
                    backend=settings.CELERY_RESULT_BACKEND,
                    broker=settings.CELERY_BROKER_URL)

celery_app.conf.imports = [
    "components.users.tasks",
    "components.auth.tasks",
]
