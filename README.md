# Interacción Gestual con Arduino: Control y Comunicación

## Descripción General

El proyecto "Interacción Gestual con Arduino: Control y Comunicación" se presenta como un sistema innovador y versátil diseñado para permitir a los usuarios controlar dispositivos externos mediante gestos de mano capturados a través de una cámara web. La convergencia de tecnologías avanzadas, como las redes neuronales convolucionales (CNN), la potente biblioteca Mediapipe para el seguimiento y análisis preciso de las manos, junto con opciones de comunicación serial y remota (a través de MQTT), establece las bases para una experiencia de interacción intuitiva y eficiente.

## Librerias

En esta sección, se importan las bibliotecas necesarias para la funcionalidad del programa:

- `cv2`: Abreviatura de OpenCV (Biblioteca de Visión por Computadora de Código Abierto), una biblioteca ampliamente utilizada para el procesamiento de imágenes y videos en visión por computadora.
- `numpy como np`: Biblioteca para operaciones numéricas y matriciales eficientes.
- `math, time`: Bibliotecas estándar de Python para operaciones matemáticas y manipulación del tiempo, respectivamente.
- `tensorflow como tf`: Biblioteca de aprendizaje profundo utilizada aquí para cargar el modelo de reconocimiento de gestos.
- `load_model` de `tensorflow.keras.models`: Función para cargar modelos preentrenados.
- `mediapipe como mp`: Biblioteca de Google para el seguimiento y análisis de objetos del mundo real, incluido el seguimiento de manos.
- `serial`: Biblioteca para la comunicación serial con dispositivos, como la conexión con Arduino.

## Carga del Modelo CNN

En esta sección, se carga un modelo de Red Neuronal Convolucional (CNN) para el reconocimiento de gestos de mano:

```python
modelo = load_model('C:\\Users\\pjrio\\proyectos\\codigo-reconocimiento-gestos-mano\\mp_gesto_mano')
```

- `load_model`: Una función de `tensorflow.keras.models` para cargar un modelo de red neuronal preentrenado.
- El modelo se carga desde la ruta especificada, en mi caso: `'C:\\Users\\pjrio\\proyectos\\codigo-reconocimiento-gestos-mano\\mp_gesto_mano'`.

## Carga de Nombres de Clase

Los nombres de clase para el modelo de reconocimiento de gestos se cargan en esta sección:

```python
con open('C:\\Users\\pjrio\\proyectos\\codigo-reconocimiento-gestos-mano\\gestos.names', 'r') as archivo:
    nombres_clase = archivo.read().split('\n')
```

- `nombres_clase` contendrá una lista de nombres de clase que el modelo puede reconocer.
- Los nombres de clase se leen desde la ruta de archivo especificada, que parece ser `'C:\\Users\\pjrio\\proyectos\\codigo-reconocimiento-gestos-mano\\gestos.names'`.

## Inicialización de Mediapipe

Mediapipe se inicializa para el seguimiento y análisis de manos:

```python
mp_dibujo = mp.solutions.drawing_utils
mp_manos = mp.solutions.hands
```

- `mp_dibujo` proporciona utilidades para dibujar en imágenes.
- `mp_manos` contiene componentes para el seguimiento y análisis de manos.

## Inicialización de la Cámara

La cámara web se inicializa para capturar video:

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

## Iniciando la Conexión Serial

Se establece una conexión serial con un dispositivo (probablemente Arduino) en esta sección:

```python
arduino = serial.Serial('COM10', 9600)
```

- `arduino`: Una instancia de `serial.Serial` para establecer comunicación serial.
- `'COM10'`: El identificador del puerto para la conexión serial.
- `9600`: La velocidad de baudios (velocidad de transmisión de datos) para la comunicación serial.

Este fragmento de código parece configurar el entorno y los recursos necesarios para el reconocimiento de gestos de mano utilizando un modelo de CNN preentrenado, Mediapipe para el seguimiento de manos y una conexión serial para la interacción con dispositivos externos.


## Envío de un Comando a través de Serial

En esta sección, se envía un comando a través de una conexión serial a un dispositivo externo (probablemente Arduino):

```python
comando = 'iniciar'
arduino.write(bytes(comando, 'utf-8'))
time.sleep(0.05)
ret = arduino.readline()
print(ret)
```

- `comando`: Una cadena que contiene el comando que se va a enviar.
- `arduino.write(bytes(comando, 'utf-8'))`: Envía el comando como bytes a través de la conexión serial establecida.
- `time.sleep(0.05)`: Pausa la ejecución durante 0.05 segundos para asegurar que el comando se transmita correctamente.
- `ret`: Almacena la respuesta recibida desde el dispositivo externo.
- `arduino.readline()`: Lee una línea (respuesta) del dispositivo externo a través de la conexión serial.
- `print(ret)`: Muestra la respuesta recibida.

En esta sección del código, se ejecuta el envío de un comando a través de una conexión serial a un dispositivo externo, probablemente Arduino. El código envía el comando, espera un breve período y luego lee y muestra la respuesta recibida del dispositivo externo.


# Iniciando bucle de captura de video

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

## Limpiando el búfer serial

En esta sección, se asegura de que no queden datos antiguos en el búfer de la conexión serial:

```python
arduino.flush()
```

- `arduino.flush()`: Limpia el búfer serial de la conexión con el dispositivo externo.

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

## Detección de manos

Aquí, se procesa la imagen para detectar las manos utilizando el componente `Hands` de Mediapipe:

```python
results = hands.process(image)
```

- `hands.process(image)`: Procesa la imagen para detectar y rastrear las manos.

## Restauración de la bandera de escritura

Después de la detección de manos, se restaura la bandera de escritura para permitir modificaciones en la imagen:

```python
image.flags.writeable = True
```

- `image.flags.writeable = True`: Configura la imagen nuevamente como escribible.

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

## Control de Arduino según el gesto detectado

En esta parte, se controla un dispositivo externo (probablemente Arduino) en función del gesto detectado:

```python
if gesture == 'thumbs down':
    # Enviar comando para detener
    # Manejar respuestas desde el dispositivo externo
elif gesture == 'thumbs up':
    # Enviar comando para avanzar
    # Manejar respuestas desde el dispositivo externo
elif send_cmd == True and finger_count == 10:
    # Enviar comando para encender luces
    # Manejar respuestas desde el dispositivo externo
```

- `gesto`: El gesto detectado.
- `enviar_comando`: Una bandera que indica si se debe enviar un comando.
- `finger_count`: Número de dedos abiertos detectados.

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
