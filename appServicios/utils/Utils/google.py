import requests
class Google(object):
    def __init__(self,token,userId):
        self.token =token
        self.userId =userId
        self.headers = {
            'Authorization': 'Bearer '+token,
            'header': 'application/json'
        }

    def request(self,url):
        response = requests.get(
                    url+self.userId,
                    headers=self.headers
                )  
        return response.json()