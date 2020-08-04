import urllib
import urllib.request
import urllib.parse


class SmsApi:
    username = ""
    password = ""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def SendSms(self, mobilenumber: str, message: str) -> str:
        """send sms via api

        Args:
            mobilenumber (str): mobile number
            message (str): message body

        Returns:
            str: status after message sending
        """
        url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
        values = {'user': self.username,
                  'passwd': self.password,
                  'message': message,
                  'mobilenumber': mobilenumber,
                  'mtype': 'N',
                  'DR': 'Y'
                  }
        data = urllib.parse.urlencode(values)
        dataStr = data.encode('utf-8')
        request = urllib.request.Request(url, dataStr)
        response = urllib.request.urlopen(request)
        return response.read().decode('utf-8')
