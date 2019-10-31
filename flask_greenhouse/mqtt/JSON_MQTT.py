import json 
import paho.mqtt.client as mqtt

send_msg = {
        'data_to_send': variable1,
        'also_send_this': variable2
}

client.publish("topic", payload=json.dumps(send_msg), qos=2, retain=False)