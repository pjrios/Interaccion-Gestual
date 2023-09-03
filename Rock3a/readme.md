
## Configuración de Callbacks MQTT
```python
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("client: " + str(client) + "userdata: " + str(userdata)+"mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
```
Estas funciones son callbacks que se utilizan en la comunicación MQTT para manejar eventos como la conexión exitosa, la publicación de mensajes, la suscripción a temas y la recepción de mensajes.

## Configuración de variables MQTT
```python
USER = "pjriosc"
PASSWORD = "arduino-conections-101"
ADDR = "4f2f4dcf13da4bd89f97a93716d25684.s2.eu.hivemq.cloud"
```
Aquí defines las credenciales y la dirección del servidor MQTT al que te conectarás.

## Configuración del cliente MQTT
```python
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(USER, PASSWORD)
client.connect(ADDR, 8883)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.subscribe("Arduino/MQTT", qos=1)
client.loop_start()
```
Estás configurando un cliente MQTT utilizando la biblioteca Paho. Esto incluye la configuración de la seguridad TLS, la conexión al servidor MQTT, y la suscripción a un tema específico ("Arduino/MQTT") con calidad de servicio (QoS) 1.

## Bucle de procesamiento de video
Dentro de este bucle, se lleva a cabo la detección de manos y el reconocimiento de gestos.

### Publicación MQTT
```python
if gesture == 'thumbs down' and enviar_comando == True:
    enviar_comando = False
    command = 'detener'
    client.publish('Arduino/MQTT', command)
    sent = False

if gesture == 'thumbs up' and enviar_comando == False:
    enviar_comando = True
    command = 'start'
    client.publish('Arduino/MQTT', command)

if enviar_comando == True and finger_count == 5 and sent == False:
    sent = True
    command = 'cinco'
    client.publish('Arduino/MQTT', command)
    time.sleep(0.01)
```
Aquí, estás publicando mensajes MQTT en función del gesto detectado y el estado de `enviar_comando` para controlar alguna acción en un dispositivo MQTT.


## Terminar y cerrar
```python
client.disconnect()
```
Finalmente, estás desconectando el cliente MQTT antes de finalizar el programa.
