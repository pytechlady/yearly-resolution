import random
import math
from pyfcm import FCMNotification
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from decouple import config
from django.core.mail import send_mail


reg_message = """<td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
          <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px;" width="29" alt="" data-proportionally-constrained="true" data-responsive="false" src="http://cdn.mcauto-images-production.sendgrid.net/954c252fedab403f/9200c1c9-b1bd-47ed-993c-ee2950a0f239/29x27.png" height="27">
        </td>
        <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
          <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px;" width="95" alt="" data-proportionally-constrained="true" data-responsive="false" src="http://cdn.mcauto-images-production.sendgrid.net/954c252fedab403f/61156dfa-7b7f-4020-85f8-a586addf4288/95x33.png" height="33">
        </td>
        <div style="font-family: inherit; text-align: center"><span style="font-size: 43px">Thanks for signing up, Jane!</span></div>
        <div style="font-family: inherit; text-align: center"><span style="font-size: 18px">Please verify your email address to</span><span style="color: #000000; font-size: 18px; font-family: arial, helvetica, sans-serif"> get access to thousands of exclusive job listings</span><span style="font-size: 18px">.</span></div>
<div style="font-family: inherit; text-align: center"><span style="color: #ffbe00; font-size: 18px"><strong>Thank you!</strong></span></div>
<td align="center" bgcolor="#ffbe00" class="inner-td" style="border-radius:6px; font-size:16px; text-align:center; background-color:inherit;">
                  <a href="" style="background-color:#ffbe00; border:1px solid #ffbe00; border-color:#ffbe00; border-radius:0px; border-width:1px; color:#000000; display:inline-block; font-size:14px; font-weight:normal; letter-spacing:0px; line-height:normal; padding:12px 40px 12px 40px; text-align:center; text-decoration:none; border-style:solid; font-family:inherit;" target="_blank">Verify Email Now</a>
                </td>
                <div style="font-family: inherit; text-align: center"><span style="color: #ffffff; font-size: 18px"><strong>Here’s what happens next:</strong></span></div>
<div style="font-family: inherit; text-align: center"><br></div>
<div style="font-family: inherit; text-align: center"><span style="color: #ffffff; font-size: 18px">1. Upload your resume and we'll keep it on file for every job submission.</span></div>
<div style="font-family: inherit; text-align: center"><br></div>
<div style="font-family: inherit; text-align: center"><span style="color: #ffffff; font-size: 18px">2. Submit and edit personalized cover letters for every job you apply to.</span></div>
<div style="font-family: inherit; text-align: center"><br></div>
<div style="font-family: inherit; text-align: center"><span style="color: #ffffff; font-size: 18px">3. Get access to our career coaches when you need 1:1 help with your job application.</span></div>
<div style="font-family: inherit; text-align: center"><span style="color: #ffbe00; font-size: 18px"><strong>+ much more!</strong></span></div>
<div style="font-family: inherit; text-align: center"><br></div>
<div style="font-family: inherit; text-align: center"><span style="color: #ffffff; font-size: 18px">Need support? Our support team is always</span></div>
<div style="font-family: inherit; text-align: center"><span style="color: #ffffff; font-size: 18px">ready to help!</span></div>
        <td align="center" bgcolor="#ffbe00" class="inner-td" style="border-radius:6px; font-size:16px; text-align:center; background-color:inherit;">
                  <a href="" style="background-color:#ffbe00; border:1px solid #ffbe00; border-color:#ffbe00; border-radius:0px; border-width:1px; color:#000000; display:inline-block; font-size:14px; font-weight:normal; letter-spacing:0px; line-height:normal; padding:12px 40px 12px 40px; text-align:center; text-decoration:none; border-style:solid; font-family:inherit;" target="_blank">Contact Support</a>
                </td>
        """


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
        send_mail(
            "Welcome to NYR - Please verify your Email",
            f"Hi there,\n\nVerify your email with the code below to start using NYR.\n\n{otp}\n\nIf you did not create a NYR account, you can ignore this message.\n\nWarm regards,\nNYR",
            config("EMAIL_HOST_USER"),
            [email_address],
        )

    @staticmethod
    def send_forgot_password_email(email_address, otp):
        message = Mail(
            from_email=config("SENDGRID_EMAIL"),
            to_emails=email_address,
            subject="Password Reset",
            html_content="""
        <h3>NYR \n \nReset your password</h3> \n \n
        
        <p>Hi there,</p> \n \n
        
        <p>You recently tried to request a password change from for your account.</p> \n \n
        
        <p>As a security measure, you need to click the link below to verify your identity</p> \n \n 
        
        <div>{otp}</div> \n \n 
        
        <p>If you do not recognize this activity, please contact us at support@NYR.com</p> \n \n
        
        <p>Warm regards,</p> \n
        
        <p>NYR</p> \n \n 
        
        <p>Copyright © 2023</p>
        """,
        )
        try:
            sg = SendGridAPIClient(config("SENDGRID_API_KEY"))
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
