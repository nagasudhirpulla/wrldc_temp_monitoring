import unittest
from src.services.smsSender import SmsApi
from src.config.appConfig import getConfig


class TestSmsSender(unittest.TestCase):

    def test_run(self) -> None:
        """tests the function that sends sms
        """
        appConfig = getConfig()
        # print(appConfig)
        smsUsername = appConfig['smsUsername']
        smsPass = appConfig['smsPassword']
        api = SmsApi(smsUsername, smsPass)
        resp: str = api.SendSms('8369949816', 'hi from python')
        self.assertTrue(resp.startswith('OK'))
