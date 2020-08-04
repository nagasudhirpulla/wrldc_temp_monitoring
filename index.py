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

# push data samples to app db
try:
    # get db config
    dbConf = getDbConfig()
    # initialize repository
    dataRepo = DeviceDataRepo(dbConf)
    # insert device data into the database
    dataRepo.insertDeviceData(dataRows)
except Exception as e:
    print('Error in pushing device data to db')
    print(e)

# check for violations and send alerts
# get the persons to send alerts
persons = getPersons()
appConfig = getConfig()
# print(appConfig)
messageSubject = 'Temperature and Humidity Violation alerts'
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

    # check for violations
    violationTypes = []
    if deviceConfig:
        devName = deviceConfig['name']
        devTemp = row['tempVal']
        devHum = row['humVal']
        tempHigh = deviceConfig['tempHigh']
        tempLow = deviceConfig['tempLow']
        humHigh = deviceConfig['humHigh']
        humLow = deviceConfig['humLow']
        if (devHum >= humHigh) or (devHum <= humLow):
            violationTypes.append('Humidity')
        if (devTemp >= tempHigh) or (devTemp <= tempLow):
            violationTypes.append('Temperature')
        if len(violationTypes) > 0:
            # create the message to be sent
            if 'Temperature' in violationTypes:
                messageBody += 'Name={0}, Temperature = {1}, thresholds = {2}, {3}<br/>'.format(
                    devName, devTemp, tempLow, tempHigh)
            if 'Humidity' in violationTypes:
                messageBody += 'Name={0}, Humidity = {1}, thresholds = {2}, {3}<br/>'.format(
                    devName, devHum, humLow, humHigh)
if not(messageBody == ""):
    messageBody = "Violations at {0}<br/>{1}".format(currTimeStr, messageBody)
    # send SMS to persons
    try:
        for prsn in persons:
            isSuccess = sendSmsToPerson(
                smsUsername, smsPass, prsn, messageBody)
    except Exception as e:
        print('Error in sending violation messages via SMS')
        print(e)

    # send email to persons
    try:
        sendEmailToPersons(
            emailUsername, emailPass, emailAddress, emailHost, persons, messageSubject, messageBody)
    except Exception as e:
        print('Error in sending violation messages via Email')
        print(e)
