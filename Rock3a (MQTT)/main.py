!pip install paho-mqtt
import paho.mqtt.client as paho
from paho import mqtt

# Configuración de MQTT
USUARIO   = "seminario-IoT2024"
CONTRASEÑA = "seminario-IoT2024"
PATH = "93fd2fab7309499aa37f1731f5d26a2a.s1.eu.hivemq.cloud"

# Define callbacks para diferentes eventos para ver si funcionan, imprimir el mensaje, etc.
def al_conectar(cliente, userdata, flags, rc, properties=None):
    print("CONNACK recibido con código %s." % rc)

# Con esta función de callback, puedes ver si tu publicación fue exitosa
def al_publicar(cliente, userdata, mid, properties=None):
    print("cliente: " + str(cliente) + " userdata: " + str(userdata) + " mid: " + str(mid))

# Imprime el tema al que se suscribió
def al_suscribir(cliente, userdata, mid, granted_qos, properties=None):
    print("Suscrito: " + str(mid) + " " + str(granted_qos))

# Imprime el mensaje, útil para verificar si fue exitoso
def al_recibir_mensaje(cliente, userdata, mensaje):
   print(mensaje.topic + " " + str(mensaje.qos) + " " + str(mensaje.payload))
   mensaje_decodificado = (mensaje.payload).decode()

   if mensaje_decodificado == "iniciar":
      comenzar()
   elif mensaje_decodificado == "detener":
      detener()

def comenzar():
    print("Comenzando el programa")

def detener():
    print("Deteniendo el programa")

# Utilizando MQTT versión 5 aquí, para 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata es datos definidos por el usuario de cualquier tipo, actualizados por user_data_set()
# client_id es el nombre dado al cliente
cliente = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
cliente.on_connect = al_conectar

# Habilitar TLS para una conexión segura
cliente.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# Establecer nombre de usuario y contraseña
cliente.username_pw_set(USUARIO, CONTRASEÑA)
# Conectar a HiveMQ Cloud en el puerto 8883 (predeterminado para MQTT)
cliente.connect(PATH, 8883)

# Configurar callbacks, utiliza funciones separadas como se muestra arriba para una mejor visibilidad
cliente.on_subscribe = al_suscribir
cliente.on_message = al_recibir_mensaje
cliente.on_publish = al_publicar

# Suscribirse a todos los temas de "Arduino/MQTT" utilizando el comodín "#"
cliente.subscribe("ROCK3A/MQTT", qos=1)

cliente.loop_forever()
