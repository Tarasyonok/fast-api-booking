from app.tasks.celery import celery
from PIL import Image
from pathlib import Path
from pydantic import EmailStr

from app.config import settings

from app.tasks.email_templates import create_booking_confirmation_template

import smtplib
from time import sleep

@celery.task()
def process_pic(
    path: str,
):
    sleep(10)
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    
    im_resized_1000_500.save(f"app/static/images/resized_1000_500{im_path.name}")
    im_resized_200_100.save(f"app/static/images/resized_200_100{im_path.name}")


# @celery.task()
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to_mock)
    
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
    
    # try:
    # YOUR_GOOGLE_EMAIL = 'snake120308@gmail.com'  # The email you setup to send the email using app password
    # YOUR_GOOGLE_EMAIL_APP_PASSWORD = 'xvpxrgctivjcovbr'  # The app password you generated

    # smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # smtpserver.ehlo()
    # smtpserver.login(YOUR_GOOGLE_EMAIL, YOUR_GOOGLE_EMAIL_APP_PASSWORD)

    # # Test send mail
    # sent_from = YOUR_GOOGLE_EMAIL
    # sent_to = sent_from  #  Send it to self (as test)
    # email_text = 'This is a test'
    # smtpserver.sendmail(sent_from, sent_to, email_text)

    # Close the connection
    # smtpserver.close()
    # except Exception:
    #     print("failed to send mail")
        