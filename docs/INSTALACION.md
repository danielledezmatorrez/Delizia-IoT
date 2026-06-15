# Instalación del Sistema Delizia IoT

## Software requerido

### Node.js
https://nodejs.org

### Node-RED
https://nodered.org

Instalar después de Node.js:

```bash
npm install -g node-red
```

### Mosquitto MQTT Broker
https://mosquitto.org/download

### InfluxDB
https://www.influxdata.com/downloads

### Grafana
https://grafana.com/grafana/download

## Ejecución

Una vez instalados todos los componentes:

1. Descargar el proyecto.
2. Ejecutar:

```txt
iniciar_delizia.bat
```

El script iniciará automáticamente:

- Mosquitto
- InfluxDB
- Node-RED
- Grafana

## Puertos utilizados

- MQTT: 1883
- Node-RED: 1880
- InfluxDB: 8086
- Grafana: 3000

## Autor

Daniel Hansel Ledezma Torrez
