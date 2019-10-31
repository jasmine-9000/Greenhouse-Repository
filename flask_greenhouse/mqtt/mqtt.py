# to install a MQTT server:
# pip install paho-mqtt
# python mqtt.py

# this code is for the broker.
#  suscribes to the broker $SYS topic tree.
# prints out the resulting messages.
import pao.mqtt.client as mqtt

#sources: 
#https://pypi.org/paho-mqtt#usage-and-api
def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	# if client disconnects, and then reconnects, it resuscribes them to the broker.
	client.suscribe("$SYS/#")

#the callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect takes the URL, the port number, and the 
client.connect("iot.eclipse.org", 1883, 60)

client.loop_forever()