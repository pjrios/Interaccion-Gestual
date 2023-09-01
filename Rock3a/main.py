#!pip install paho-mqtt

import paho.mqtt.client as paho
from paho import mqtt

# MQTT
USER     = "pjriosc"
PASSWORD = "arduino-conections-101"

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("client: " + str(client) + "userdata: " + str(userdata)+"mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
   print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
   mensage_decodificado = (msg.payload).decode() 

   if(mensage_decodificado== "start"):
      starting()
   elif(mensage_decodificado== "detener"):
      stoping()


def starting(): 
    print("Comenzando el programa")

def stoping(): 
    print("Deteniendo el programa")

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(USER, PASSWORD)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("4f2f4dcf13da4bd89f97a93716d25684.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("Arduino/MQTT", qos=1)
i=0
seguir=True
client.loop_start()
while(seguir):
	if(i<90000):
		i=+1
		#print(i)
	else:
		seguir=False
client.loop_stop()



