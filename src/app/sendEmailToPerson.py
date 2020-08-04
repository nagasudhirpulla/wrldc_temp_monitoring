from src.config.appConfig import PersonInfo
from src.services.emailSender import EmailSender
from typing import List


def sendEmailToPersons(emailUsername: str, emailPass: str, emailAddress: str, emailHost: str, prsns: List[PersonInfo], messageSubject: str, messageBody: str) -> None:
    """Send Email to a Persons List

    Args:
        emailUsername (str): [description]
        emailPass (str): [description]
        emailAddress (str): [description]
        emailHost (str): [description]
        prsns (List[PersonInfo]): [description]
        messageSubject (str): [description]
        messageBody (str): [description]
    """
    emailApi = EmailSender(emailAddress, emailUsername, emailPass, emailHost)
    emailApi.sendEmail([prsn['mail']
                        for prsn in prsns], messageSubject, messageBody)
