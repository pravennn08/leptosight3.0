import json
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def send_otp_template(phone_number, token):

    try:
        client = Client(
            os.getenv("TWILIO_ACCOUN_SID"),
            os.getenv("TWILIO_AUTH_TOKEN"),
        )
        # message = (
        #     f"LeptoSight: Your verification code is {token}. "
        #     f"This code expires in 3 minutes. "
        #     f"Do not share this code with anyone."
        # )

        message = client.messages.create(
            from_=os.getenv("TWILIO_SENDER"),
            to=f"whatsapp:+{phone_number}",
            # body=message,
            content_sid=os.getenv("TWILIO_CONTENT_SID"),
            content_variables=json.dumps({"1": token}),
        )
        print("OTP sent successfully:", message.sid)
        return message.sid
    except Exception as error:
        print(error)
        return None
