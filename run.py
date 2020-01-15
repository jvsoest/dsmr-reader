# Before first execution, please run
# curl -XPOST 'http://localhost:8086/query' --data-urlencode 'q=CREATE DATABASE meterstanden'

from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
from dsmr_parser import obis_references
import time
import requests

devicePath = '/dev/ttyUSB1'
sleepTime = 10
varsToCollect = ["ELECTRICITY_USED_TARIFF_1", "ELECTRICITY_USED_TARIFF_2", "ELECTRICITY_ACTIVE_TARIFF", "CURRENT_ELECTRICITY_USAGE", "HOURLY_GAS_METER_READING"]
#varsToCollect = ["P1_MESSAGE_TIMESTAMP", "ELECTRICITY_USED_TARIFF_1", "ELECTRICITY_USED_TARIFF_2", "ELECTRICITY_ACTIVE_TARIFF", "CURRENT_ELECTRICITY_USAGE", "HOURLY_GAS_METER_READING"]

def connectReader(deviceName):
    return SerialReader(
        device=deviceName,
        serial_settings=SERIAL_SETTINGS_V5,
        telegram_specification=telegram_specifications.V5
    )

serial_reader = connectReader(devicePath)

abort = False
errorCount = 0

while not abort:
    try:
        for telegram in serial_reader.read_as_object():
            timestamp = int(round(time.time() * 1000000000))
            for attribute in varsToCollect:
                value = str(getattr(telegram, attribute).value)
                unit = str(getattr(telegram, attribute).unit)
                #print(attribute + " | " + value)

                resultPost = requests.post("http://localhost:8086/write?db=meterstanden",
                                data="standen,variable=%s,unit=%s value=%s %s" % (attribute, unit, value, timestamp),
                                headers={"Content-Type": "application/x-www-form-urlencoded"})
                #print(str(resultPost.text))
            errorCount = 0
            break
    except:
        print("Something went wrong when reading meter output, reconnecting meter")
        serial_reader = None
        serial_reader = connectReader(devicePath)
        errorCount += 1
    
    # next second of retrieval is always sleepTime + 1 therefore removing 1 second
    time.sleep(sleepTime - 1)

    if errorCount > 5:
        abort = True
