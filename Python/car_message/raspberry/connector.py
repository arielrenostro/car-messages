import serial as serial

from car_message.raspberry.settings import BLUETOOTH_SERIAL_DEVICE, BLUETOOTH_SERIAL_TIMEOUT


class Connector:

    _serial = None

    def __init__(self):
        super().__init__()
        self._serial = serial.Serial(port=BLUETOOTH_SERIAL_DEVICE, timeout=BLUETOOTH_SERIAL_TIMEOUT)

    def connect(self):
        if not self._serial.is_open:
            self._serial.open()

    def close(self):
        if self._serial.is_open:
            self._serial.close()

    def write(self, data):
        if isinstance(data, str):
            data = bytes(data.encode("utf-8"))

        if not isinstance(data, bytes):
            data = bytes(data)

        return self._try_until_fail(fn=self._serial.write, data=data)

    def read(self, size=1):
        return self._try_until_fail(fn=self._serial.read, size=size)

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
