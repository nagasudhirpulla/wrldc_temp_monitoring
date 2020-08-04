import pandas as pd
from typing import TypedDict, List


class AppConfig(TypedDict):
    emailAddress: str
    emailUsername: str
    emailPassword: str
    emailHost: str
    smsUsername: str
    smsPassword: str


class DeviceConfig(TypedDict):
    name: str
    ip: str
    tempHigh: float
    tempLow: float
    humHigh: float
    humLow: float


class PersonInfo(TypedDict):
    name: str
    mail: str
    phone: float


class DbConfig(TypedDict):
    dbName: str
    host: str
    port: int
    username: str
    password: str


def getConfig(configFilename='config.xlsx', sheetName='config') -> AppConfig:
    """[summary]
    Get the application config from config.xlsx file
    Returns:
        dict: The application configuration as a dictionary
    """

    df = pd.read_excel(configFilename, header=None,
                       index_col=0, sheet_name=sheetName)
    configDict = df[1].to_dict()
    return configDict


def getDbConfig(configFilename='config.xlsx', sheetName='dbConfig') -> DbConfig:
    """[summary]
    Get the application config from config.xlsx file
    Returns:
        dict: The application db configuration as a dictionary
    """

    df = pd.read_excel(configFilename, header=None,
                       index_col=0, sheet_name=sheetName)
    configDict = df[1].to_dict()
    return configDict


def getPersons(configFilename='config.xlsx', sheetName='persons') -> List[PersonInfo]:
    """List of persons from config

    Args:
        configFilename (str, optional): Defaults to 'config.xlsx'.
        sheetName (str, optional): Defaults to 'persons'.

    Returns:
        List[PersonInfo]: list of person info objects
    """
    personsDf = pd.read_excel(configFilename, sheet_name=sheetName)
    return personsDf.to_dict('records')


def getDevices(configFilename='config.xlsx', sheetName='devices') -> List[DeviceConfig]:
    """Get the list of devices from config excel

    Args:
        configFilename (str, optional): Defaults to 'config.xlsx'.
        sheetName (str, optional): Defaults to 'devices'.

    Returns:
        List[DeviceConfig]: list of device config objects
    """
    devicesDf = pd.read_excel(configFilename, sheet_name=sheetName)
    return devicesDf.to_dict('records')
