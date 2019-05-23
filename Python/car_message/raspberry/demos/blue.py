import sys
import bluetooth

sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

bt_addr = "A8:16:D0:EF:1E:4A"
port = 0x1001

print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

sock.connect((bt_addr, port))

print("connected.  type stuff")
while True:
    data = input()
    if len(data) == 0:
        break
    sock.send(data)
    data = sock.recv(1024)
    print("Data received:", str(data))

sock.close()