# https://stackoverflow.com/questions/34653875/python-how-to-send-data-over-tcp
# https://stackoverflow.com/questions/4666973/how-to-extract-the-substring-between-two-markers
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.isnull.html
import socket
import re
from typing import TypedDict, List, Optional


class DeviceInfo(TypedDict):
    temp: Optional[float]
    hum: Optional[float]


def fetchDeviceCurrentData(devIp: str) -> DeviceInfo:
    """This service gets the device data at current time

    Args:
        devIp (str): ip address of the device

    Returns:
        DeviceInfo: current device info
    """
    tempVal = None
    humVal = None
    port = 4567
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((devIp, port))
        s.sendall(b's')
        data = s.recv(1024).decode("utf-8")
        s.close()
        # get humidity value
        m = re.search('.*t2=(.+?)$', data)
        if m:
            humVal = float(m.group(1))
        # get temp value
        m = re.search('.*t1=(.+?)&.*', data)
        if m:
            tempVal = float(m.group(1))
    except:
        tempVal = None
        humVal = None
    return {"temp": tempVal, "hum": humVal}
