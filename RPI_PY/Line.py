import requests

class LINE:
    def __init__(self, token='svdr3xFLuKKbVhrD1wW0UyQrb4t1CBMR6mjyN9xfay8'):
        print("HELLO IT ME!")
        self.token = token
        self.endpoint = "https://notify-api.line.me/api/notify"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + self.token}
    
    def send(self,text):
        r = requests.post(self.endpoint, headers=self.headers, data={'message': text})
        return (r.text,r.status_code)
    
    def __del__(self):
        print("LINE Object has been destroyed")
