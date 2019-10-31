import paho.mqtt.subscribe as subscribe

msg = suscribe.simple("paho/test/simple",hostname="iot.eclipse.org")
print("%s %s" % (msg.topic, msg.payload))

