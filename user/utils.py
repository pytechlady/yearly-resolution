import random
import math
from pyfcm import FCMNotification
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config


class Util:
    
    @staticmethod
    def generate_otp():
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP

    @staticmethod
    def send_notification(registration_id, message_title, message_body):
        push_service = FCMNotification(api_key="<api-key>")
        resp = push_service.notify_single_device(
            registration_id=registration_id,
            message_title=message_title,
            message_body=message_body,
        )
        return resp

    @staticmethod
    def send_registration_email(email_address, otp):
        message = Mail(
        from_email=config('SENDGRID_EMAIL'),
        to_emails=email_address,
        subject="Welcome to NYR - Please verify your Email",
        html_content='''
        <h3>Verify your email address</h3> \n \n
        
        <p>Hi there,</p> \n \n
        
        <p>Verify your email with the code below to start using NYR.</p> \n \n
        
        <div>{otp}</div> \n \n
        
        <p>If you did not create a NYR account, you can ignore this message.</p> \n \n
        
        <p>Warm regards,NYR</p> \n \n
        
        <p>Copyright © 2023</p>
        
        ''')
        try:
            sg = SendGridAPIClient(api_key =config('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))

    @staticmethod
    def send_forgot_password_email(email_address, otp):
        message = Mail(
        from_email=config('SENDGRID_EMAIL'),
        to_emails=email_address,
        subject="Password Reset",
        html_content='''
        <h3>NYR \n \nReset your password</h3> \n \n
        
        <p>Hi there,</p> \n \n
        
        <p>You recently tried to request a password change from for your account.</p> \n \n
        
        <p>As a security measure, you need to click the link below to verify your identity</p> \n \n 
        
        <div>{otp}</div> \n \n 
        
        <p>If you do not recognize this activity, please contact us at support@NYR.com</p> \n \n
        
        <p>Warm regards,</p> \n
        
        <p>NYR</p> \n \n 
        
        <p>Copyright © 2023</p>
        ''')
        try:
            sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))

    @staticmethod
    def generate_referral_link():
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        link = ""
        for i in range(8):
            link += letters[math.floor(random.random() * 52)]
        return link
