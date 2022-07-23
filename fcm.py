import json
from decouple import config
import requests

class Fcm():
    def send(self,deviceToken,title,body,dataPayLoad=None):
        serverToken=config('fcm_server_key')
        deviceToken=deviceToken
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
        }
        
        body = {
          'notification': {'title': title,
                            'body': body,
                            'icon':"https://pulse-api-bucket.s3.amazonaws.com/static/72+x+72.png"
                          },
          'to':
              deviceToken,
          'priority': 'high',
          'data': dataPayLoad,
        }
        response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
        print(response.status_code)
        print(response.json())
