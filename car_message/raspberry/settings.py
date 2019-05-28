import os

MAX_MESSAGES_PER_REQUEST = 20
CAR = "GOL_G4_2009_MFBXXXX"

BLUETOOTH = {
    'DEVICE': '/dev/rfcomm0',
    'TIMEOUT': 2,
    'BAUDRATE': 115200,
}

ENDPOINTS = {
    'SEND_MESSAGE': {
        'URL': os.getenv('ENDPOINT_SEND_MESSAGE'),
        'X-API-KEY': os.getenv('ENDPOINT_SEND_MESSAGE_KEY')
    }
}

CONNECTOR = {
    'ENDLINE': {
        'ACTIVE': True,
        'FORMAT': b'\r\n'
    }
}