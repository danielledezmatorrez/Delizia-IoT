import paho.mqtt.client as mqtt
import json
import time
import random
import math

BROKER    = "localhost"
PORT      = 1883
TOPICO    = "delizia/produccion/ambiental"
INTERVALO = 10  # reducido a 10 segundos para demo rápida

BASE_TEMP = 22.0
BASE_HUM  = 55.0
BASE_CO2  = 750

contador      = 0
modo_alerta   = False
ciclos_alerta = 0
ciclos_normal = 0

def generar_datos():
    global contador, modo_alerta, ciclos_alerta, ciclos_normal
    contador += 1

    # Cada 8 envíos activa alerta durante 4 ciclos
    # luego 6 ciclos normal y vuelve a alertar
    if not modo_alerta and ciclos_normal <= 0 and contador % 8 == 0:
        modo_alerta   = True
        ciclos_alerta = 4
        ciclos_normal = 6
        print("\n⚠  ALERTA ACTIVADA — Condición crítica detectada\n")

    if modo_alerta:
        ciclos_alerta -= 1
        if ciclos_alerta <= 0:
            modo_alerta = False
            print("\n✓  CONDICIÓN NORMALIZADA — Enviando datos normales\n")
        return {
            "node_id":       "ESP32-01",
            "area":          "produccion",
            "temperature_c": round(random.uniform(46.0, 49.0), 1),
            "humidity_pct":  round(random.uniform(86.0, 90.0), 1),
            "co2_ppm":       random.randint(5100, 5800),
            "rssi_dbm":      random.randint(-75, -45)
        }

    if ciclos_normal > 0:
        ciclos_normal -= 1

    hora_simulada  = (contador * INTERVALO / 3600) % 24
    variacion_hora = math.sin(hora_simulada * math.pi / 12) * 3

    return {
        "node_id":       "ESP32-01",
        "area":          "produccion",
        "temperature_c": round(BASE_TEMP + variacion_hora + random.uniform(-0.5, 0.5), 1),
        "humidity_pct":  round(BASE_HUM  - variacion_hora + random.uniform(-2.0, 2.0), 1),
        "co2_ppm":       int(BASE_CO2 + variacion_hora * 50 + random.randint(-50, 50)),
        "rssi_dbm":      random.randint(-75, -45)
    }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ Conectado al broker MQTT")
    else:
        print(f"✗ Error de conexión: código {rc}")

def on_publish(client, userdata, mid):
    print(f"  → Mensaje enviado (id={mid})")

cliente = mqtt.Client(client_id="simulador-delizia-01")
cliente.on_connect = on_connect
cliente.on_publish = on_publish

print("=" * 50)
print("  SIMULADOR ESP32 — Sistema IoT Delizia")
print("=" * 50)
print(f"  Broker   : {BROKER}:{PORT}")
print(f"  Tópico   : {TOPICO}")
print(f"  Intervalo: {INTERVALO}s")
print("  Ciclo: 8 normales → 4 alertas → 6 normales")
print("  Presiona Ctrl+C para detener")
print("=" * 50)

try:
    cliente.connect(BROKER, PORT, keepalive=60)
    cliente.loop_start()

    while True:
        datos   = generar_datos()
        payload = json.dumps(datos)
        cliente.publish(TOPICO, payload, qos=1)

        estado = "⚠  ALERTA" if modo_alerta else "✓  Normal"
        print(f"\n[#{contador}] {estado}")
        print(f"  Temperatura : {datos['temperature_c']} °C")
        print(f"  Humedad     : {datos['humidity_pct']} %")
        print(f"  CO2         : {datos['co2_ppm']} ppm")
        print(f"  Señal WiFi  : {datos['rssi_dbm']} dBm")

        time.sleep(INTERVALO)

except KeyboardInterrupt:
    print("\n\nSimulador detenido.")
except ConnectionRefusedError:
    print("\n✗ ERROR: No se pudo conectar al broker.")
    print("  Verifica que Mosquitto esté corriendo.")
finally:
    cliente.loop_stop()
    cliente.disconnect()