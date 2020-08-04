from src.config.appConfig import getDevices
from src.services.deviceDataFetcher import fetchDeviceCurrentData
from src.repos.deviceData import DeviceDataSample, DeviceDataRepo
from typing import List
import datetime as dt
from src.config.appConfig import getDbConfig, getConfig, getPersons
from src.services.smsSender import SmsApi
from src.app.sendSmsToPerson import sendSmsToPerson
from src.app.sendEmailToPerson import sendEmailToPersons

# get devices from config
devicesList = getDevices()

# get current time
currTime = dt.datetime.now()
currTimeStr = dt.datetime.strftime(currTime, '%d-%m-%Y, %H:%M:%S')

# initialize samples array for insertion
dataRows: List[DeviceDataSample] = []

# collect data from each device
for dvce in devicesList:
    devCurrData = fetchDeviceCurrentData(dvce['ip'])
    tempVal = devCurrData['temp']
    humVal = devCurrData['hum']
    # consider only if data is not None
    if not((humVal == None) or (tempVal == None)):
        devDataRecord: DeviceDataSample = {
            'name': dvce['name'],
            'timestamp': currTime,
            'tempVal': devCurrData['temp'],
            'humVal': devCurrData['hum']
        }
        dataRows.append(devDataRecord)
# print(dataRows)

# get the persons to send alerts
persons = getPersons()
appConfig = getConfig()
# print(appConfig)
messageSubject = 'Temperature and Humidity alerts'
# create the message to be sent
messageBody = ""
# sms credentials
smsUsername = appConfig['smsUsername']
smsPass = appConfig['smsPassword']
# email credentials
emailUsername = appConfig['emailUsername']
emailPass = appConfig['emailPassword']
emailAddress = appConfig['emailAddress']
emailHost = appConfig['emailHost']

for row in dataRows:
    # get device configuration
    deviceConfig = next(
        (d for d in devicesList if d['name'] == row['name']), None)

    if deviceConfig:
        devTemp = row['tempVal']
        devHum = row['humVal']
        devName = deviceConfig['name']
        messageBody += 'Name = {0}, Temperature = {1}, Humidity = {2}<br/>'.format(
            devName, devTemp, devHum)

if not(messageBody == ""):
    messageBody = "Time={0}<br/>{1}".format(currTimeStr, messageBody)
    try:
        for prsn in persons:
            isSuccess = sendSmsToPerson(
                smsUsername, smsPass, prsn, messageBody)
    except Exception as e:
        print('Error in sending messages via SMS')
        print(e)

    # send email to persons
    try:
        sendEmailToPersons(
            emailUsername, emailPass, emailAddress, emailHost, persons, messageSubject, messageBody)
    except Exception as e:
        print('Error in sending messages via Email')
        print(e)
