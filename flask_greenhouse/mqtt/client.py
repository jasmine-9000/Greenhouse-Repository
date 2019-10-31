#to publish a message to the broker, use these functions.
#
# pip install paho-mqtt
# 
import paho.mqtt.publish as publish

topic = "$SYS$"
publish.single(topic, payload=None, qos=0,retain=False, hostname="localhost",
port=1883,client_id="",keepalive=60,will=None, auth=None, tls=None,
protocol=mqtt.MQTTv311,transport="tcp")
