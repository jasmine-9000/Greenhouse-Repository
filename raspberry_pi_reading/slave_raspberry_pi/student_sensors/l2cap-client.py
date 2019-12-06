import bluetooth

sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)

bd_addr = "01:23:45:67:89:AB"
port = 0x1001

sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()