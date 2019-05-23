import time
from functools import reduce
from threading import Thread

import serial as serial

from car_message.raspberry.settings import BLUETOOTH_SERIAL_DEVICE, BLUETOOTH_SERIAL_TIMEOUT, COMMANDS


class UpdateConnectorThread(Thread):

    _connector = None

    def __init__(self, connector):
        super().__init__()
        self._connector = connector

    def run(self):
        while True:
            serial_ = self._connector._serial
            buffer_ = self._connector._buffer

            if not serial_.is_open:
                serial_.open()

            if serial_.is_open:
                data = serial_.read(size=1024)
                if data is not None:
                    for d in data:
                        buffer_.append(chr(d))


class Connector:

    _serial = None
    _buffer = list()

    def __init__(self):
        self._serial = serial.Serial(port=BLUETOOTH_SERIAL_DEVICE, timeout=BLUETOOTH_SERIAL_TIMEOUT)
        self._thread = UpdateConnectorThread(self)
        self._thread.start()

    def receive_raw(self):
        data_buffer = self._buffer
        self._buffer = list()
        return reduce((lambda x, y: f'{x}{y}'), data_buffer)

    def receive_line(self):
        buffer = ""
        data = None
        while not data == '\n':
            if data is not None:
                buffer += data
                data = None
            else:
                time.sleep(0.1)

            if len(self._buffer) > 0:
                data = self._buffer.pop(0)

        return buffer

    def receive_command(self, commands=COMMANDS):
        idx = 0
        buffer = ""

        while buffer not in commands:
            if idx == len(self._buffer):
                return None

            buffer += self._buffer[idx]
            idx += 1

        for i in range(idx - 1):
            self._buffer.pop(0)
        return buffer

    def send(self, data):
        if isinstance(data, str):
            data = bytes(data.encode("utf-8"))

        if not isinstance(data, bytes):
            data = bytes(data)

        self._try_until_fail(fn=self._serial.write, data=data)

    def close(self):
        self._serial.close()

    @classmethod
    def _try_until_fail(cls, fn, **kwargs):
        count = 0
        while count < 5:
            try:
                return fn(**kwargs)
                break
            except Exception as e:
                print(str(e))
                count += 1


connector = Connector()
