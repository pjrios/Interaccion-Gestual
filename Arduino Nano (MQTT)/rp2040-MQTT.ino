#include <WiFiNINA.h>
#include <PubSubClient.h>
#include "credentials.h"

#define TOPIC "Arduino/MQTT"

// MQTT Configuration
const char* mqtt_server = "broker.hivemq.com";
const int mqttPort = 1883;
const char* mqttUser = "pjriosc";
const char* mqttPassword = "arduino-conexiones-101"; // Insert your password

//WiFi
char ssid[] = SSID;
char password[] = PASSKEY;

// Status
int status = WL_IDLE_STATUS;

int led1_status = 0;

WiFiClient wifiClient;
PubSubClient client(wifiClient);
byte mac[6];  
long lastMsg = 0;
char msg[100];
int value = 0;

void setup() {
  delay(10000);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqttPort);
  client.setCallback(callback);
  pinMode(8,OUTPUT);
  digitalWrite(8,LOW);
}

void setup_wifi() {

  delay(1000);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.macAddress(mac);
  Serial.println();
  Serial.print("Mac address ");
  int i = 0;
  for(i = 0; i<6; i++){
    Serial.println(mac[i],HEX);
  }
  Serial.println();
  


  while (status != WL_CONNECTED) {
    //status = WiFi.begin(ssid, password);
    status = WiFi.begin(ssid, password);

  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  // Convert the payload to a string
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  // Print the received message
  Serial.println(message);
  
  int val = digitalRead(8);
  Serial.print("Current LED status: ");
  Serial.println(val);
  
  if (val) {
    digitalWrite(8, LOW);
  } else {
    digitalWrite(8, HIGH);
  }
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "Arduino RP2040 Client";
    // Attempt to connect
    if (client.connect(mqttUser)){
      Serial.println("connected");
      // Once connected, subscribe to input channel
      client.subscribe(TOPIC);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(100);
}
