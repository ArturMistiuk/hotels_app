import smtplib
from pathlib import Path
from typing import NoReturn

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_setup import celery_worker
from app.tasks.email_templates import create_booking_confirmation_template


@celery_worker.task
def process_pic(
        path: str
) -> NoReturn:
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((100, 200))
    im_resized_1000_500.save(f'app/static/images/resized_1000_500_{im_path.name}')
    im_resized_200_100.save(f'app/static/images/resized_200_100_{im_path.name}')


@celery_worker.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr,
) -> NoReturn:
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
