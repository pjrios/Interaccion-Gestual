#include <Servo.h>  // Incluir la librería Servo para controlar el servo motor

Servo servo1;                         // Crear un objeto servo llamado 'servo1'
const int servoPin = 9;               // Pin digital utilizado para el control del servo
const unsigned long duracion = 5000; // Duración del movimiento en milisegundos (10 segundos)
const int toleranciaAngulo = 2;       // Tolerancia de diferencia de ángulo para considerar que el movimiento ha finalizado
const int duracionRetardo = 5;       // Retardo para un movimiento suave del servo

unsigned long tiempoInicial;          // Tiempo en que comenzó el movimiento
bool enMoviendo = false;              // Variable para indicar si el servo está en movimiento
int anguloFinal = 0;                  // Ángulo final al que se moverá el servo

void setup() {
  Serial.begin(9600);                 // Inicializar la comunicación serial a 9600 baudios
  servo1.attach(servoPin);            // Asociar el pin del servo al objeto 'servo1'
  servo1.write(0);                    // Establecer la posición inicial del servo en 0 grados
  digitalWrite(2, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String entrada = Serial.readStringUntil('\n');  // Leer la entrada serial hasta encontrar un salto de línea

    Serial.println(entrada);

    if (entrada == "start" && !enMoviendo) {         // Si se recibe "diez" y no hay un movimiento en curso
      iniciarMovimientoServo(0);                  // Iniciar movimiento del servo a 180 grados 
      digitalWrite(2, HIGH);
      Serial.println(entrada);
    }

    if (entrada == "diez" && !enMoviendo) {         // Si se recibe "diez" y no hay un movimiento en curso
      iniciarMovimientoServo(180);                  // Iniciar movimiento del servo a 180 grados
      digitalWrite(2, HIGH);
      Serial.println(entrada);
    }

    if (entrada == "uno" && !enMoviendo) {          // Si se recibe "uno" y no hay un movimiento en curso
      iniciarMovimientoServo(90);                   // Iniciar movimiento del servo a 90 grados
      digitalWrite(2, HIGH);
      Serial.println(entrada);
    }
    if (entrada == "detener" && !enMoviendo) {      // Si se recibe "detener" y no hay un movimiento en curso
      iniciarMovimientoServo(0);                    // Iniciar movimiento del servo a 0 grados (detener)
      digitalWrite(2, HIGH);
      Serial.println(entrada);
    }
  }
  
  if (enMoviendo) {                                  // Si hay un movimiento en curso
    unsigned long tiempoActual = millis();           // Obtener el tiempo actual en milisegundos
    if (tiempoActual - tiempoInicial <= duracion) {  // Si no ha pasado el tiempo de duración del movimiento
      int anguloActual = map(tiempoActual - tiempoInicial, 0, duracion, 0, anguloFinal);  // Calcular el ángulo actual basado en el tiempo transcurrido
      servo1.write(anguloActual);                    // Mover el servo al ángulo actual
      delay(duracionRetardo);                        // Introducir un pequeño retardo para suavizar el movimiento del servo
    } else if (abs(anguloFinal - servo1.read()) < toleranciaAngulo) {  // Si ha pasado el tiempo de duración y el servo está cerca del ángulo final
      enMoviendo = false;  // Finalizar el movimiento
    }
  }
}

void iniciarMovimientoServo(int angulo) {
  servo1.write(0);  // Establecer la posición inicial del servo en 0 grados antes de iniciar el movimiento
  anguloFinal = angulo;      // Establecer el ángulo final deseado
  tiempoInicial = millis();  // Registrar el tiempo en que comenzó el movimiento
  enMoviendo = true;         // Indicar que se ha iniciado el movimiento
}
