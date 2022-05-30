from config.celery_app import celery_app


@celery_app.task
def send_mail_forgot_password(email: str, valid_token: str):
    print("email: ", email)
    print("Token: ", valid_token)