import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT   = 1883
TOPICO = "delizia/produccion/ambiental"

cliente = mqtt.Client(client_id="probador-alertas")

# Validación: verificar conexión al broker MQTT
try:
    cliente.connect(BROKER, PORT)
    print("✓ Conexión al broker MQTT exitosa")
except Exception as e:
    print(f"✗ No se pudo conectar al broker MQTT: {e}")
    print("  Verifica que Mosquitto esté corriendo.")
    exit(1)

escenarios = {
    "1": {"nombre": "Normal",             "temperature_c": 24.0, "humidity_pct": 55.0, "co2_ppm": 750},
    "2": {"nombre": "ALERTA temperatura", "temperature_c": 47.0, "humidity_pct": 55.0, "co2_ppm": 750},
    "3": {"nombre": "ALERTA humedad",     "temperature_c": 24.0, "humidity_pct": 88.0, "co2_ppm": 750},
    "4": {"nombre": "ALERTA CO2",         "temperature_c": 24.0, "humidity_pct": 55.0, "co2_ppm": 5500},
    "5": {"nombre": "CRISIS total",       "temperature_c": 50.0, "humidity_pct": 90.0, "co2_ppm": 6000},
}

normal = {"temperature_c": 24.0, "humidity_pct": 55.0, "co2_ppm": 750}

def enviar(datos, veces, intervalo, etiqueta):
    payload = json.dumps({
        "node_id":       "ESP32-01",
        "area":          "produccion",
        "temperature_c": datos["temperature_c"],
        "humidity_pct":  datos["humidity_pct"],
        "co2_ppm":       datos["co2_ppm"],
        "rssi_dbm":      -60
    })
    for i in range(veces):
        cliente.publish(TOPICO, payload, qos=1)
        print(f"  [{i+1}/{veces}] {etiqueta} — T:{datos['temperature_c']}°C  H:{datos['humidity_pct']}%  CO2:{datos['co2_ppm']}ppm")
        time.sleep(intervalo)

print("\n=== PROBADOR DE ALERTAS — Delizia ===\n")
while True:
    print("Elige un escenario:")
    for k, v in escenarios.items():
        print(f"  {k}) {v['nombre']}")
    print("  6) DEMO COMPLETA (Firing + Resolved automático)")
    print("  0) Salir")

    opcion = input("\nOpción: ").strip()

    if opcion == "0":
        break

    elif opcion == "6":
        print("\n🔴 FASE 1 — Enviando alerta durante 30 segundos...")
        enviar(escenarios["2"], 10, 3, "⚠ ALERTA")
        print("\n✅ FASE 2 — Enviando valores normales durante 40 segundos...")
        enviar(normal, 8, 5, "✓ Normal")
        print("\n✓ Demo completa — revisa tu email\n")

    elif opcion in escenarios:
        e = escenarios[opcion]
        print(f"\nEnviando {e['nombre']} durante 18 segundos...")
        enviar(e, 6, 3, e["nombre"])
        print("✓ Listo\n")

    else:
        print("Opción inválida.\n")

cliente.disconnect()
print("Listo.")