from src.config.appConfig import PersonInfo
from src.services.smsSender import SmsApi


def sendSmsToPerson(smsUsername: str, smsPass: str, prsn: PersonInfo, messageBody: str) -> bool:
    """Send SMS to a Person

    Args:
        smsUsername (str): username of API
        smsPass (str): Password of API
        prsn (PersonInfo): Person object
        messageBody (str): Message Body

    Returns:
        bool: whether the process is success
    """
    api = SmsApi(smsUsername, smsPass)
    resp: str = api.SendSms(
        prsn['phone'], messageBody.replace('<br/>', '. '))
    if resp.startswith('OK'):
        return True
    else:
        return False
