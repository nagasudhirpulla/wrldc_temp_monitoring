import unittest
from src.services.emailSender import EmailSender
from src.config.appConfig import getConfig


class TestEmailSender(unittest.TestCase):

    def test_run(self) -> None:
        """tests the function that sends sms
        """
        appConfig = getConfig()
        # print(appConfig)
        emailUsername = appConfig['emailUsername']
        emailPass = appConfig['emailPassword']
        emailAddress = appConfig['emailAddress']
        emailHost = appConfig['emailHost']
        emailApi = EmailSender(
            emailAddress, emailUsername, emailPass, emailHost)
        emailApi.sendEmail(
            ['nagasudhir@posoco.in'], "Testing email sender in python", 'Hello from python script!')
        self.assertTrue(1 == 1)
