from typing import TypedDict, List
import psycopg2
import datetime as dt
from src.config.appConfig import DbConfig


class DeviceDataSample(TypedDict):
    name: str
    timestamp: dt.datetime
    tempVal: float
    humVal: float


class DeviceDataRepo():
    """
    table name - devices_time_data
    columns - data_time, device_name, temp_val, hum_val
    """
    dbConfig: DbConfig = {
        "dbName": "",
        "host": "",
        "port": 0,
        "username": "",
        "password": ""
    }

    def __init__(self, dbConf: DbConfig) -> None:
        """constructor method

        Args:
            dbConf (DbConfig): database configuration object
        """        
        self.dbConfig = dbConf

    def insertDeviceData(self, devData: List[DeviceDataSample]) -> None:
        """inserts device data rows to application db

        Args:
            devData (List[DeviceDataSample]): rows to be inserted
        """        
        conn = psycopg2.connect(host=self.dbConfig['host'],
                                dbname=self.dbConfig['dbName'],
                                user=self.dbConfig['username'],
                                password=self.dbConfig['password'])
        # Create data tuples
        dataInsertionTuples = []
        for rowItr in range(len(devData)):
            dataRow = devData[rowItr]
            insTup = (dt.datetime.strftime(dataRow['timestamp'], '%Y-%m-%d %H:%M:%S'), dataRow['name'],
                      dataRow['tempVal'], dataRow['humVal'])
            dataInsertionTuples.append(insTup)

        # get cursor for insertion
        cur = conn.cursor()

        # prepare sql for insertion and execute
        dataText = ','.join(cur.mogrify('(%s,%s,%s,%s)', row).decode(
            "utf-8") for row in dataInsertionTuples)

        # create insertion sql
        sqlTxt = """insert into devices_time_data(data_time, device_name, temp_val, hum_val)
                    values {0} on conflict (data_time, device_name) 
                    do update set temp_val = excluded.temp_val, hum_val=excluded.hum_val""".format(dataText)
        cur.execute(sqlTxt)
        conn.commit()
