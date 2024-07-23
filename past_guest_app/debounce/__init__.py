import re
import requests, os
from normalization import Norm_Email

class Debounce:
    def __init__(self):
        self.url = os.environ.get('DEBOUNCE_URL') if os.environ.get('DEBOUNCE_URL') else "https://api.debounce.io/v1/"
        self.key = os.environ.get('DEBOUNCE_APIKEY') if os.environ.get('DEBOUNCE_APIKEY') else "60d159908ed0f"
        self.headers = {'Accept': 'application/json'}
        self.querystring = {'api': self.key}

    def validonce(self, email):
        """
            {
                "debounce": {
                    "email": "rich@gemail.com",
                    "code": "6",
                    "role": "false",
                    "free_email": "false",
                    "result": "Invalid",
                    "reason": "Bounce",
                    "send_transactional": "0",
                    "did_you_mean": "rich@gmail.com"
                },
                "success": "1",
                "balance": "966769"
            }
        """
        self.querystring.update({"email": Norm_Email(email)})
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
        print(response)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "debounce": {
                    "email": Norm_Email(email),
                    "code": "10",
                    "role": "false",
                    "free_email": "false",
                    "result": "Invalid",
                    "reason": "HandShacke Fail",
                    "send_transactional": "0",
                    "did_you_mean": ""
                }
            }

    def balance(self):
        """
            {
                "balance": "966769"
            }
        """
        response = requests.request("GET", self.url+'balance/', headers=self.headers, params=self.querystring)
        return response.json()

    def disposable(self, email):
        """"
            {
                "disposable": "false"
            }
        """
        url = "https://disposable.debounce.io/"
        self.querystring = {"email": Norm_Email(email)}
        response = requests.request("GET", url, headers=self.headers, params=self.querystring)
        return response.json()



    """
    {
        "debounce": {
            "email": "rich@gemail.com",
            "code": "6",
            "role": "false",
            "free_email": "false",
            "result": "Invalid",
            "reason": "Bounce",
            "send_transactional": "0",
            "did_you_mean": "rich@gmail.com"
        },
        "success": "1",
        "balance": "966769"
    }
    """
