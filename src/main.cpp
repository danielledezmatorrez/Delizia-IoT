#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
 
// ─────────────────────────────────────────────────────────────
//  CONFIGURACIÓN — edita solo estas 4 líneas
// ─────────────────────────────────────────────────────────────
const char* WIFI_SSID     = "NOMBRE_DE_TU_WIFI";
const char* WIFI_PASSWORD = "CONTRASEÑA_WIFI";
const char* MQTT_BROKER   = "192.168.1.XXX"; // IP de tu PC
const char* NODE_ID       = "ESP32-01";       // cambia por nodo
// ─────────────────────────────────────────────────────────────
 
const char* AREA         = "produccion";
const int   MQTT_PORT    = 1883;
#define DHT_PIN           4    // pin DATA del DHT22
#define DHT_TYPE          DHT22
#define MQ135_PIN         34   // pin analógico del MQ-135
#define INTERVALO_MS      30000 // 30 segundos entre lecturas
 
DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient   wifiClient;
PubSubClient mqtt(wifiClient);
 
float ultimaTemp = 22.0;
float ultimaHum  = 50.0;
 
// ── Conexión WiFi ────────────────────────────────────────────
void conectarWiFi() {
  Serial.print("\nConectando WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 30) {
    delay(500);
    Serial.print(".");
    intentos++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi OK. IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\nError WiFi — reiniciando...");
    ESP.restart();
  }
}
 
// ── Conexión MQTT ────────────────────────────────────────────
void conectarMQTT() {
  int intentos = 0;
  while (!mqtt.connected() && intentos < 5) {
    Serial.print("Conectando MQTT...");
    String clientId = "ESP32-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    if (mqtt.connect(clientId.c_str())) {
      Serial.println("OK");
    } else {
      Serial.println("fallo rc=" + String(mqtt.state()) + " reintento en 3s");
      delay(3000);
      intentos++;
    }
  }
}
 
// ── Leer sensores ────────────────────────────────────────────
float leerTemperatura() {
  float t = dht.readTemperature();
  if (isnan(t)) {
    Serial.println("Error DHT22 temp — usando ultimo valor");
    return ultimaTemp;
  }
  ultimaTemp = t;
  return t;
}
 
float leerHumedad() {
  float h = dht.readHumidity();
  if (isnan(h)) {
    Serial.println("Error DHT22 hum — usando ultimo valor");
    return ultimaHum;
  }
  ultimaHum = h;
  return h;
}
 
int leerGases() {
  // Lectura raw del ADC (0-4095). Para convertir a ppm
  // se necesita calibración con gas de referencia.
  // Por ahora devolvemos el valor raw mapeado.
  int raw = analogRead(MQ135_PIN);
  return map(raw, 0, 4095, 400, 5000); // mapeo aproximado a ppm CO2
}
 
// ── Publicar por MQTT ─────────────────────────────────────────
void publicarDatos(float temp, float hum, int co2) {
  StaticJsonDocument<256> doc;
  doc["node_id"]       = NODE_ID;
  doc["area"]          = AREA;
  doc["temperature_c"] = round(temp * 10.0) / 10.0; // 1 decimal
  doc["humidity_pct"]  = round(hum  * 10.0) / 10.0;
  doc["co2_ppm"]       = co2;
  doc["rssi_dbm"]      = WiFi.RSSI();
 
  char payload[256];
  serializeJson(doc, payload);
 
  char topico[64];
  snprintf(topico, sizeof(topico), "delizia/%s/ambiental", AREA);
 
  bool ok = mqtt.publish(topico, payload, true); // retain=true
  if (ok) {
    Serial.println("✓ Publicado: " + String(payload));
  } else {
    Serial.println("✗ Error al publicar");
  }
}
 
// ── Setup ────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== Sistema IoT Delizia ===");
  Serial.println("Nodo: " + String(NODE_ID));
 
  dht.begin();
  analogSetAttenuation(ADC_11db); // para lecturas 0-3.3V en MQ-135
 
  conectarWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setKeepAlive(60);
  conectarMQTT();
 
  Serial.println("Sistema listo. Enviando datos cada 30s");
}
