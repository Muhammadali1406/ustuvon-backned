from celery import shared_task


@shared_task(name="users.send_verification_code")
def send_verification_code_task(user_id: str, code: str, channel: str, purpose: str) -> None:
    from apps.notifications.services import send_verification_message
    send_verification_message(user_id=user_id, code=code, channel=channel, purpose=purpose)