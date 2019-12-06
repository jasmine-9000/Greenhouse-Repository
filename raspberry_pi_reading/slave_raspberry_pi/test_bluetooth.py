import bluetooth

my_bluetooth_address = "60:9A:C1:F3:79:74"

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
	if my_bluetooth_address == bdaddr:
		print(bluetooth.lookup_name(bdaddr))
