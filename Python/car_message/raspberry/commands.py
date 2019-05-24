from enum import Enum


class RequestMode(Enum):
    SHOW_CURRENT_DATA = 0x01


class RequestPID(Enum):
    RPM = 0x0C
    SPEED = 0x0D
    COOLANT_TEMPERATURE = 0x05
    INTAKE_AIR_TEMPERATURE = 0x0F


PID_RESPONSE_SIZE = {
    RequestPID.RPM: 4,
    RequestPID.SPEED: 3,
    RequestPID.COOLANT_TEMPERATURE: 3,
    RequestPID.INTAKE_AIR_TEMPERATURE: 3,
}

PID_RESPONSE_CONVERTER = {
    RequestPID.RPM: (lambda x: ((x[3] * 256) + x[4]) / 4),
    RequestPID.SPEED: (lambda x: x[3]),
    RequestPID.COOLANT_TEMPERATURE: (lambda x: x[3] - 40),
    RequestPID.INTAKE_AIR_TEMPERATURE: (lambda x: x[3] - 40),
}

SUCCESS_RESPONSE = 0x41
