import os

BLUETOOTH_SERIAL_DEVICE = '/dev/rfcomm0'
BLUETOOTH_SERIAL_TIMEOUT = 1


CAR = {
    'NAME': 'GOL_G4_2009_MFB-XXXX'
}

ENDPOINTS = {
    'SEND_MESSAGE': {
        'URL': os.getenv('ENDPOINT_SEND_MESSAGE'),
        'X-API-KEY': os.getenv('ENDPOINT_SEND_MESSAGE_KEY')
    }
}
