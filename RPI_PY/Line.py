import requests

class LINE:
    def __init__(self, token : str):
        self.token = token
        self.endpoint = "https://notify-api.line.me/api/notify"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + self.token}
    
    def send(self,text : str):
        r = requests.post(self.endpoint, headers=self.headers, data={'message': text})
        return (r.text,r.status_code)
