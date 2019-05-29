import binascii
import time
from datetime import datetime
from threading import Thread

import requests

from connector import Connector
from commands import (
    RequestMode,
    RequestPID,
    PID_RESPONSE_SIZE,
    SUCCESS_RESPONSE,
    PID_RESPONSE_CONVERTER
)
from settings import CAR, ENDPOINTS, CONNECTOR, MAX_MESSAGES_PER_REQUEST


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

    byte_command = bytearray(request)

    decoded = binascii.hexlify(byte_command).decode('utf-8')

    if CONNECTOR['ENDLINE']['ACTIVE']:
        decoded += CONNECTOR['ENDLINE']['FORMAT'].decode("utf-8")

    response_size = len(decoded)  # Echo command
    response_size += (PID_RESPONSE_SIZE[pid] * 2)  # Multiply by 2 because response is HEX
    response_size += 1  # Always end with '>'
    if CONNECTOR['ENDLINE']['ACTIVE']:
        response_size += len(CONNECTOR['ENDLINE']['FORMAT']) * 2  # End have 2 breaklines

    return decoded, response_size


def handle_response(request, pid, command, data, response_raw, second_time=False):
    if 'NO DATA' in response_raw:
        print("Module is not configured!")
        init_eml327(connector)
        return request_command(connector, request, pid, data)

    while 'SEARCHING...' in response_raw:
        delay = 2
        print(f"Module is not ready. Retrying in {delay}s...")
        time.sleep(delay)
        return request_command(connector, request, pid, data)

    parsed_response = parse_response(command, response_raw)

    if len(parsed_response) == PID_RESPONSE_SIZE[pid] \
            and parsed_response[0] == SUCCESS_RESPONSE \
            and parsed_response[1] == pid.value:
        converter = PID_RESPONSE_CONVERTER[pid]
        converted_value = converter(parsed_response)
        print(f"Converted response: {converted_value}")
        return converted_value

    elif second_time:
        print(f'Invalid response {response_raw}')

    else:
        response_raw += connector.read(1024).decode('utf-8')
        return handle_response(request, pid, command, data, response_raw, True)


def request_command(connector: Connector, request: RequestMode, pid: RequestPID, data: bytearray = None):
    command, response_size = make_command(request, pid, data)

    print(f"Sending to bluetooth: {str(repr(command))}")
    connector.write(command)

    response_raw = connector.read(response_size).decode('utf-8')
    print(f"Received from bluetooth: {repr(response_raw)}")

    return handle_response(request, pid, command, data, response_raw)


def parse_response(command, response):
    command_size = len(command)

    try:
        return bytes.fromhex(response[command_size:-5])
    except ValueError as e:
        print(e)
        return ''


def init_eml327(connector, sleep=2):
    print("Initializing EML327...")

    command = "ATSP0"
    if CONNECTOR['ENDLINE']['ACTIVE']:
        command += CONNECTOR['ENDLINE']['FORMAT'].decode('utf-8')
    connector.write(command)  # Set to find protocol
    time.sleep(sleep)
    response = connector.read(1024).decode("utf-8")
    if 'ATSP0' not in response or 'OK' not in response:
        print(f'Retrying! Received {response}')
        init_eml327(connector, sleep+1)
        return

    print("Initialized!")


def send_payload():
    while True:
        payloads_to_send = []

        size = len(payloads)
        if size > MAX_MESSAGES_PER_REQUEST:
            size = MAX_MESSAGES_PER_REQUEST

        for i in range(size - 1):
            payloads_to_send.append(
                payloads.pop(0)
            )

        if len(payloads_to_send) > 0:
            response = requests.post(
                url=ENDPOINTS['SEND_MESSAGE']['URL'],
                headers={
                    'x-api-key': ENDPOINTS['SEND_MESSAGE']['X-API-KEY'],
                    'Content-Type': 'application/json'
                },
                json=payloads_to_send
            )
            print(response)

        time.sleep(5)


print('======================')
print('= Car Bluetooth OBD2 =')
print('= Ariel Adonai Souza =')
print('======================')

payloads = []
connector = Connector()
sender = Thread(target=send_payload)
sender.start()

while True:
    rpm = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.RPM)
    speed = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.SPEED)
    coolant_temperature = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.COOLANT_TEMPERATURE)
    intake_temperature = request_command(connector, RequestMode.SHOW_CURRENT_DATA, RequestPID.INTAKE_AIR_TEMPERATURE)

    payload = {
        'datetime': datetime.utcnow().strftime("%Y/%m/%dT%H:%M:%S.%fZ"),
        'car': CAR,
        'speed': speed,
        'rpm': rpm,
        'intakeTemperature': intake_temperature,
        'coolantTemperature': coolant_temperature,
    }

    print(f"{payload}")
    payloads.append(payload)
