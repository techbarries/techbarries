from twilio.rest import Client
from decouple import config


class Twilio():
    def __init__(self, sms,phone):
        self.sms = sms
        self.phone = phone

    def send(self):            
        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token=config('TWILIO_AUTH_TOKEN')
        from_number=config('TWILIO_FROM_NUMBER')
        client = Client(account_sid, auth_token)
        try:
            message = client.messages \
                            .create(
                                body=self.sms,
                                from_=from_number,
                                to=self.phone
                            )
            if message.sid is not None:
                return 1
            else:
                return 0                
        except:
            return 2
   