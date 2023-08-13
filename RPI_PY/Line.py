"""
 
    LINE Utilities Senders Python Modules
    Features:
        - Senders text
  
    @author (TheNongice Wasawat)
    LICENSE: MIT License
    Dates: 13/8/2023 - 0:17

"""

import requests

class LINE:
    def __init__(self, token : str):
        self.token = token
        self.endpoint = "https://notify-api.line.me/api/notify"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + self.token}
    
    def send(self,text : str, Stop_Nofication: bool = False):
        r = requests.post(
            self.endpoint, 
            headers=self.headers, 
            data={
                'message': text,
                'notificationDisabled': Stop_Nofication
            }
        )
        return (r.text,r.status_code)

    def change_token(self, token : str):
        self.token = token
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + self.token}
