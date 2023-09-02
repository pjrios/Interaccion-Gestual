# Antes de comenzar
Este projecto esta escrito en Python y Arduino. En caso que necesistes informacion sobre la instalacion y uso de python puedes visitar este repositorio: [Python 101](https://github.com/pjrios/Python-101/tree/main)

# Interacción Gestual con Arduino y Rock3a: Control y Comunicación

## Descripción General

Este proyecto se enfoca en desarrollar un sistema interactivo que permite a los usuarios controlar dispositivos externos, utilizando un Arduino y un Rock3a, a través de gestos de mano detectados por una cámara. La combinación de tecnologías como redes neuronales convolucionales (CNN), la biblioteca Mediapipe para el detección y análisis de manos, y la comunicación serial o MQTT, facilita la interacción entre el usuario y los dispositivos.
Table of contents:

[[_TOC_]]

## Librerias

Para este projecto utilizamos las siguientes librerias:

1. **`cv2 (OpenCV)`**:
   - Descripción: OpenCV (Open Source Computer Vision Library) es una biblioteca de visión por computadora de código abierto que proporciona una amplia gama de funciones para el procesamiento de imágenes y videos en tiempo real.
   - Utilidad: Se utiliza para tareas como manipulación de imágenes, detección y seguimiento de objetos, reconocimiento facial, calibración de cámaras y más en aplicaciones de visión por computadora.

2. **`numpy (np)`**:
   - Descripción: NumPy es una biblioteca fundamental para la computación científica en Python. Proporciona un soporte eficiente para matrices multidimensionales y operaciones matemáticas en ellas.
   - Utilidad: Se utiliza para realizar cálculos numéricos y matriciales de manera rápida y eficiente, lo que es esencial en muchas aplicaciones científicas y de análisis de datos.

3. **`math`**:
   - Descripción (math): El módulo `math` es una biblioteca estándar de Python que proporciona funciones matemáticas básicas.
   - Utilidad (math): Se utiliza para realizar operaciones matemáticas, como funciones trigonométricas, logaritmos, etc.
4. **`time`**:
   - Descripción (time): El módulo `time` es una biblioteca estándar de Python que se utiliza para trabajar con operaciones relacionadas con el tiempo.
   - Utilidad (time): Se utiliza para medir intervalos de tiempo, programar tareas, manejar fechas y horas, y otras operaciones relacionadas con el tiempo.

5. **`tensorflow (tf)`**:
   - Descripción: TensorFlow es una biblioteca de aprendizaje profundo (deep learning) desarrollada por Google. Proporciona herramientas y funciones para construir y entrenar modelos de aprendizaje profundo.
   - Utilidad: Se utiliza para construir y entrenar modelos de redes neuronales, realizar inferencias en modelos preentrenados y realizar tareas de aprendizaje profundo en general.

6. **`load_model de tensorflow.keras.models`**:
   - Descripción: `load_model` es una función proporcionada por el módulo `tensorflow.keras.models` que se utiliza para cargar modelos de aprendizaje profundo previamente entrenados y almacenados en disco.
   - Utilidad: Se utiliza para cargar modelos previamente entrenados y utilizarlos para realizar inferencias en nuevos datos sin tener que volver a entrenar el modelo.

7. **`mediapipe (mp)`**:
   - Descripción: MediaPipe es una biblioteca desarrollada por Google que proporciona soluciones de seguimiento y análisis de objetos del mundo real, como manos, rostros, posturas, etc.
   - Utilidad: Se utiliza para rastrear y analizar objetos en tiempo real, lo que es especialmente útil en aplicaciones de realidad aumentada, interacción humano-computadora y más.

8. **`serial`**:
   - Descripción: La biblioteca `serial` se utiliza para la comunicación serial entre dispositivos, como la conexión con placas de desarrollo como Arduino.
   - Utilidad: Se utiliza para establecer una comunicación bidireccional entre un ordenador y dispositivos externos mediante puertos seriales, permitiendo la transferencia de datos en tiempo real.

9. **`paho-mqtt`**:
   - Descripción: Paho MQTT es una biblioteca que implementa el protocolo MQTT (Message Queuing Telemetry Transport) para la comunicación entre dispositivos conectados a Internet de las Cosas (IoT).
   - Utilidad: Se utiliza para establecer conexiones y enviar mensajes entre dispositivos a través del protocolo MQTT, lo que es esencial en aplicaciones de IoT para transmitir datos de manera eficiente y confiable.


## Cargar el Modelo de Red Neuronal Convolucional (CNN)

Para el reconocimiento de gestos, se puden utilizar modelos publicos, entrenar uno nuevo, o modificar modelos existentes. Pueden encontrar modelos en la [pagina official de Keras](https://tfhub.dev/). En este caso utilizare un modelo publico de Red Neuronal Convolucional ( o Convolutional Neural Network, CNN) para el reconocimiento de gestos de mano:

```python
# Recuerden cambiar la ubicacion de ejemplo.
modelo = load_model('C:\\Usuario\\ubicacion\\del\\archivo\\codigo-reconocimiento-gestos-mano\\mp_gesto_mano')
```

- `load_model`: Una función de `tensorflow.keras.models` para cargar un modelo de red neuronal preentrenado.
- El modelo se carga desde la ruta especificada, en mi caso: `'C:\\Users\\pjrio\\proyectos\\codigo-reconocimiento-gestos-mano\\mp_gesto_mano'`.

## Cargar los Nombres de la Clase

Los nombres de clase para el modelo de reconocimiento de gestos se cargan en esta sección:

```python
# Recuerden cambiar la ubicacion de ejemplo.
con open('C:\\Usuario\\ubicacion\\del\\archivo\\codigo-reconocimiento-gestos-mano\\gestos.names', 'r') as archivo:
    nombres_clase = archivo.read().split('\n')
```

- `nombres_clase` contiene una lista de nombres de clase que el modelo puede reconocer.
- Los nombres de clase se leen desde la ruta de archivo especificada, en mi caso ser `'C:\\Users\\pjrio\\proyectos\\codigo-reconocimiento-gestos-mano\\gestos.names'`.

## Inicialización de Mediapipe

Mediapipe se inicializa para el seguimiento y análisis de manos:

```python
mp_dibujo = mp.solutions.drawing_utils
mp_manos = mp.solutions.hands
```

- `mp_dibujo` proporciona utilidades para dibujar en imágenes.
- `mp_manos` contiene componentes para el seguimiento y análisis de manos.

## Inicialización de la Cámara

La cámara se inicializa para capturar video:

```python
cap = cv2.VideoCapture(0)
```

- `cap`: Una instancia de `cv2.VideoCapture` para capturar video desde la cámara predeterminada (índice 0).

## Variables

Configuración de variables iniciales:

```python
enviar_comando = False
ret = 'ninguno'
```

- `enviar_comando`: Una bandera que indica si debe enviarse un comando.
- `ret`: Una variable para almacenar una respuesta.

# Bucle de captura de video

En esta sección, se inicia un bucle para capturar video desde la cámara y procesar los frames para el reconocimiento de gestos de mano utilizando la biblioteca `mediapipe` y OpenCV:

```python
with mp_manos.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
```

- `mp_manos.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands`: Inicializa el componente de detección y seguimiento de manos de Mediapipe con las confianzas mínimas especificadas.
- `cap.isOpened()`: Verifica si la captura de video está en curso.
- `ret`: Variable booleana que indica si el frame se capturó correctamente.
- `frame`: El frame de video actual.


## Conversión de formato de color y volteo horizontal

En esta sección, se realiza el preprocesamiento de la imagen del frame capturado:

```python
image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
image = cv2.flip(image, 1)
```

- `cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)`: Convierte el formato de color de BGR a RGB.
- `cv2.flip(image, 1)`: Voltea horizontalmente la imagen para visualización natural.

## Configuración de la bandera de escritura

En esta parte, se configura la bandera de escritura de la imagen para garantizar que no se modifiquen los datos:

```python
image.flags.writeable = False
```

- `image.flags.writeable = False`: Configura la imagen como no escribible.
- `image.flags.writeable = True`: Configura la imagen nuevamente como escribible.

## Detección de manos

Aquí, se procesa la imagen para detectar las manos utilizando el componente `Hands` de Mediapipe:

```python
results = hands.process(image)
```

- `hands.process(image)`: Procesa la imagen para detectar y rastrear las manos.


## Conversión de formato de color

Aquí, se convierte la imagen de nuevo al formato BGR para poder trabajar con las funciones de dibujo de OpenCV:

```python
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
```

- `cv2.cvtColor(image, cv2.COLOR_RGB2BGR)`: Convierte la imagen de RGB a BGR.

## Conteo de dedos y detección de gestos

En esta sección, se analizan los resultados de la detección de manos para contar dedos y detectar gestos:

```python
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        # Mediciones de distancias entre puntos clave
        # Cálculos para contar dedos abiertos
        # Dibujo de landmarks en la imagen
        # Predicción de gestos basada en landmarks
```

- `results.multi_hand_landmarks`: Verifica si se detectaron manos en el frame.
- `hand_landmarks`: Puntos clave (landmarks) detectados en la mano.



## Mostrar información en la imagen

Aquí, se agrega información al frame visualizado, como el conteo de dedos y la detección de gestos:

```python
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(image, f'Conteo de Dedos: {finger_count}', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
cv2.putText(image, f'Gesto: {gesture}', (10, 70), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
cv2.putText(image, f'Enviar Habilitado: {send_cmd} && Enviado {sent}', (10, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
```

- `cv2.putText(image, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)`: Agrega texto al frame visualizado.
- `text`: El texto a mostrar.
- `(x, y)`: Posición del texto en el frame.
- `font`: Fuente del texto.
- `scale`: Escala del texto.
- `color`: Color del texto.
- `thickness`: Grosor del texto.
- `cv2.LINE_AA`: Tipo de antialiasing para el texto.

## Mostrar el frame de salida

Finalmente, se muestra el frame procesado con la información y los resultados:

```python
cv2.imshow('Seguimiento de Mano y Reconocimiento de Gesto', image)
```

- `cv2.imshow(window_name, image)`: Muestra la imagen en una ventana con el nombre especificado.

## Romper el bucle y liberar recursos

Al final, el bucle se rompe si se presiona la tecla 'q', y se liberan los recursos de la cámara y las ventanas:

```python
if cv2.waitKey(10) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
```

- `cv2.waitKey(delay)`: Espera una tecla presionada durante el tiempo especificado en milisegundos.
- `ord('q')`: Valor numérico de la tecla 'q'.
- `cap.release()`: Libera los recursos de la cámara.
- `cv2.destroyAllWindows()`: Cierra todas las ventanas abiertas.
