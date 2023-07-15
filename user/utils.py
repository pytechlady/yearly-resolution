import random
import math
from pyfcm import FCMNotification
from django.core.mail import EmailMessage


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
        email_body = f'''
        Verify your email address
        
        Hi there,
        
        Verify your email with the code below to start using NYR. 
        
        \t \t \t{otp}\t \t \t 
        
        If you did not create a NYR account, you can ignore this message.
        
        Warm regards,NYR
        
        Copyright © 2023
        '''
        email_subject = "Welcome to NYR - Please verify your Email"
        data = {
            "email_body": email_body,
            "to_email": email_address,
            "email_subject": email_subject,
        }
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()

    @staticmethod
    def send_forgot_password_email(email_address, otp):
        email_body = f"NYR \n \nReset your password \n \nHi there, \nYou recently tried to request a password change from for your account. As a security measure, you need to click the link below to verify your identity \n \n {otp} \n \n If you do not recognize this activity, please contact us at support@NYR.com or simply reply to this email to secure your account. \n \nWarm regards, \nNYR \n \n Copyright © 2023"
        email_subject = "Welcome to NYR - Please verify your Email"
        data = {
            "email_body": email_body,
            "to_email": email_address,
            "email_subject": email_subject,
        }
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()
        
    @staticmethod
    def generate_referral_link():
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        link = ""
        for i in range(8):
            link += letters[math.floor(random.random() * 52)]
        return link
