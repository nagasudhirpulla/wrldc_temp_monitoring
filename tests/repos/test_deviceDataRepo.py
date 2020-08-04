import unittest
from src.repos.deviceData import DeviceDataRepo,  DeviceDataSample
from src.config.appConfig import getDbConfig
import datetime as dt


class TestFetchOutages(unittest.TestCase):

    def test_run(self) -> None:
        """tests the device data repository operations
        """
        # get db config
        dbConf = getDbConfig()
        devDataRepo = DeviceDataRepo(dbConf)
        # insert a test row
        testRow: DeviceDataSample = {
            'name': 'test',
            'timestamp': dt.datetime(2000, 1, 1),
            'tempVal': -1,
            'humVal': -1
        }
        devDataRepo.insertDeviceData([testRow])
        self.assertTrue(1 == 1)
