import unittest
from src.services.deviceDataFetcher import fetchDeviceCurrentData


class TestFetchDeviceData(unittest.TestCase):

    def test_run(self) -> None:
        """tests the function that fetches the current device data
        """
        ip = '10.2.100.72'
        devData = fetchDeviceCurrentData(ip)
        # print(devData)
        self.assertTrue('temp' in devData)
        self.assertTrue('hum' in devData)
        self.assertFalse(devData['temp'] == None)
        self.assertFalse(devData['hum'] == None)
