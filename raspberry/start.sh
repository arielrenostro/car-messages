BLUETOOTH_MAC="00:1D:A5:68:98:8A"

rfcomm release 0
rfcomm bind 0 ${BLUETOOTH_MAC}

python3 app.py