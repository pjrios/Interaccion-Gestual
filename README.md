

# Antes de comenzar
Este projecto esta escrito en Python y Arduino. En caso que necesistes informacion sobre la instalacion y uso de python puedes visitar este repositorio: [Python 101](https://github.com/pjrios/Python-101/tree/main)

## Descripción General del Script
Este script en Python proporciona una solución para la supervisión de datos de sensores y la interacción con el modelo de lenguaje GPT-3 de OpenAI a través de MQTT. A continuación, se presenta un resumen de las principales funciones y características del script:

```markdown
## Importando Dependencias

```python
!pip install paho-mqtt openai
import paho.mqtt.client as mqtt
import openai
import time
import random
from datetime import datetime
```

Esta sección instala los paquetes de Python necesarios utilizando `pip` e importa las bibliotecas necesarias para la comunicación MQTT, la integración con OpenAI y otras funcionalidades.

---

## Funciones de Callback MQTT

```python
# Configuración de Callbacks MQTT
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK recibido con código %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("cliente: " + str(client) + " userdata: " + str(userdata) + " mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Suscrito: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
```

Estas funciones definen el comportamiento de las devoluciones de llamada MQTT cuando ocurren eventos diferentes, como la conexión al broker, la publicación, la suscripción y la recepción de mensajes.

---

## Configuración MQTT

```python
# Configuración de variables MQTT
USUARIO = "pjriosc"
CONTRASEÑA = "arduino-conexiones-101"
DIRECCION = "4f2f4dcf13da4bd89f97a93716d25684.s2.eu.hivemq.cloud"

# Inicializamos el cliente MQTT
cliente = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
cliente.on_connect = on_connect

cliente.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
cliente.username_pw_set(USUARIO, CONTRASEÑA)
cliente.connect(DIRECCION, 8883)

cliente.on_subscribe = on_subscribe
cliente.on_message = on_message
cliente.on_publish = on_publish

cliente.subscribe("Arduino/MQTT", qos=1)
cliente.loop_start()
```

Esta sección configura los parámetros de conexión MQTT e inicializa el cliente MQTT con la configuración adecuada. También configura devoluciones de llamada MQTT para varios eventos y se suscribe a un tema específico.

---

## Configuración e Inicialización de Datos del Sensor

```python
# Configuración (puedes cargar estos datos desde variables de entorno o un archivo de configuración)
direccion_broker_mqtt = "mqtt.ejemplo.com"
puerto_mqtt = 1883
tema_mqtt = "sensor/datos"
clave_api_openai = "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"
umbral_temperatura = 2.0  # Umbral ajustable para el cambio de temperatura

# Inicializar valores anteriores para la detección de cambios
temperatura_anterior = 25.0
humedad_anterior = 50.0

# Inicializar datos simulados del sensor
temperatura_simulada = 25.0
humedad_simulada = 50.0
```

Esta parte define los parámetros de configuración, incluidos los ajustes de MQTT, la clave de la API de OpenAI y el umbral de temperatura. También inicializa variables para almacenar datos anteriores del sensor y simula lecturas iniciales del sensor.

---

## Configuración de la Clave de API de OpenAI

```python
# Configurar tu clave de API de OpenAI
openai.api_key = clave_api_openai
```

Aquí, el código configura la clave de API de OpenAI para su uso posterior en la interacción con el modelo ChatGPT.

---

## Gestión de Datos del Sensor

```python
# Inicializar una lista para almacenar lecturas del sensor con (temperatura, humedad, marca de tiempo)
lecturas_del_sensor = []
```

Esta sección inicializa una lista vacía para almacenar lecturas del sensor, cada una compuesta por temperatura, humedad y marca de tiempo.

---

## Función de Publicación de Datos del Sensor

```python
# Definir una función para leer datos del sensor y agregarlos a la lista
def publicar_datos_del_sensor():
    global temperatura_anterior, humedad_anterior, temperatura_simulada, humedad_simulada, lecturas_del_sensor

    # Simular datos del sensor aquí
    # (La temperatura aumenta cada 1 segundo, la humedad disminuye cada 2 segundos)
    
    # Obtener la marca de tiempo actual

    # Agregar los datos simulados a la lista con la marca de tiempo

    # Publicar datos simulados a MQTT

    # Comprobar cambios significativos y solicitar una explicación
```

Esta función simula datos del sensor, los agrega a la lista `lecturas_del_sensor`, los publica en MQTT y verifica cambios significativos en la temperatura y la humedad.

---

## Detección de Cambios y Solicitud de Explicación

```python
# Definir una función para verificar cambios significativos y solicitar una explicación a ChatGPT
def verificar_cambios(nueva_temperatura, nueva_humedad):
    global temperatura_anterior, humedad_anterior

    # Ejemplo: si la temperatura aumentó más que el umbral
    
    # Actualizar los valores anteriores para la próxima comprobación
```

Esta función verifica si hay un cambio significativo en la temperatura y la humedad en comparación con las lecturas anteriores. Si hay un cambio significativo, solicita una explicación a ChatGPT.

---

## Interacción con ChatGPT

```python
# Definir una función para interactuar con ChatGPT
def charlar_con_gpt(prompt):
    respuesta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50  # Ajustar según sea necesario
    )
    return respuesta.choices[0].text
```

Esta función interactúa con ChatGPT utilizando la API de OpenAI, proporcionando un estímulo y recibiendo una respuesta.

---

## Bucle Principal

```python
# Conéctate al broker MQTT y comienza el bucle de monitoreo
cliente.connect("4f2f4dcf13da4bd89f97a93716d25684.s2.eu.hivemq.cloud", 8883)
cliente.loop_start()
segundos = 0

# Bucle principal para publicar datos del sensor
try:
    while True:
        # Recopilar datos del sensor y enviarlos a ChatGPT cada 1
