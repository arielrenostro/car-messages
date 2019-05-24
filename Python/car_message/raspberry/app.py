from datetime import datetime

import requests

from connector import Connector
from commands import (
    RequestMode,
    RequestPID,
    PID_RESPONSE_SIZE,
    SUCCESS_RESPONSE,
    PID_RESPONSE_CONVERTER
)
from settings import CAR, ENDPOINTS


def make_command(request: RequestMode, pid: RequestPID, data: bytearray = None):
    if not request or not pid:
        raise AttributeError(f'Invalid command. Missing request or pid')

    request = [
        request.value,
        pid.value,
    ]

    if data:
        if isinstance(data, (list, set)):
            for d in data:
                request.append(d)
        else:
            request.append(data)

    return bytearray(request)


def request_command(connector: Connector, request: RequestMode, pid: RequestPID, data: bytearray = None):
    command = make_command(request, pid, data)

    connector.write(command)

    size_response = PID_RESPONSE_SIZE[pid]
    response = connector.read(size_response)

    if len(response) == size_response \
            and response[0] == SUCCESS_RESPONSE \
            and response[1] == pid.value:
        converter = PID_RESPONSE_CONVERTER[pid]
        return converter(response)


print('======================')
print('= Car Bluetooth OBD2 =')
print('= Ariel Adonai Souza =')
print('======================')

connector = Connector()

while True:
    rpm = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.RPM)
    speed = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.SPEED)
    coolant_temperature = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.COOLANT_TEMPERATURE)
    intake_temperature = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.INTAKE_AIR_TEMPERATURE)

    payload = {
        'datetime': datetime.utcnow().strftime("%Y/%m/%dT%H:%M:%SZ"),
        'car': CAR['NAME'],
        'speed': speed,
        'rpm': rpm,
        'intakeTemperature': intake_temperature,
        'coolantTemperature': coolant_temperature,
    }

    response = requests.post(
        url=ENDPOINTS['SEND_MESSAGE']['URL'],
        headers={
            'x-api-key': ENDPOINTS['SEND_MESSAGE']['X-API-KEY'],
            'Content-Type': 'application/json'
        },
        json=payload
    )

    print(response)

