from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
from dsmr_parser import obis_references
import time


sleepTime = 5
varsToCollect = ["P1_MESSAGE_TIMESTAMP", "ELECTRICITY_USED_TARIFF_1", "ELECTRICITY_USED_TARIFF_2", "ELECTRICITY_ACTIVE_TARIFF", "CURRENT_ELECTRICITY_USAGE", "HOURLY_GAS_METER_READING"]

serial_reader = SerialReader(
    device='/dev/ttyUSB1',
    serial_settings=SERIAL_SETTINGS_V5,
    telegram_specification=telegram_specifications.V5
)

abort = False

while not abort:
    for telegram in serial_reader.read_as_object():
        for attribute in varsToCollect:
            print(attribute + " | " + str(getattr(telegram, attribute).value))
        break
    
    # next second of retrieval is always sleepTime + 1 therefore removing 1 second
    time.sleep(sleepTime - 1)
