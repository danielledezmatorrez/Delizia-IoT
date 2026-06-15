# Delizia IoT

## Descripción

Sistema IoT para monitoreo ambiental en tiempo real utilizando ESP32, MQTT, Node-RED, InfluxDB y Grafana.

## Tecnologías utilizadas

- ESP32
- PlatformIO
- MQTT (Mosquitto Broker)
- Node-RED
- InfluxDB
- Grafana

## Arquitectura

ESP32 → MQTT Broker (Mosquitto) → Node-RED → InfluxDB → Grafana

## Archivos del proyecto

- src/ : Código fuente ESP32
- include/ : Archivos de cabecera
- lib/ : Librerías del proyecto
- test/ : Pruebas
- platformio.ini : Configuración PlatformIO
- iniciar_delizia.bat : Script de inicio automático

## Ejecución

Ejecutar:

iniciar_delizia.bat

Este script inicia automáticamente:

1. Mosquitto MQTT Broker
2. InfluxDB
3. Node-RED
4. Grafana

## Interfaces

- InfluxDB: http://localhost:8086
- Node-RED: http://localhost:1880
- Grafana: http://localhost:3000

## Requisitos

Para ejecutar el proyecto se requiere tener instalados:

- Node.js
- Node-RED
- Mosquitto MQTT Broker
- InfluxDB
- Grafana

## Autor

Daniel Hansel Ledezma Torrez
