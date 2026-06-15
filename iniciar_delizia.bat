@echo off
title Sistema IoT - Delizia
color 0A

echo ============================================
echo    SISTEMA IoT DELIZIA - INICIANDO...
echo ============================================
echo.

echo [1/4] Iniciando Mosquitto...
start "MQTT Broker" cmd /k ""C:\Program Files\mosquitto\mosquitto.exe" -v"

timeout /t 5 /nobreak > nul

echo [2/4] Iniciando InfluxDB...
start "InfluxDB" cmd /k "cd /d ""C:\Program Files\InfluxData\influxdb"" && influxd.exe"

timeout /t 10 /nobreak > nul

echo [3/4] Iniciando Node-RED...
start "Node-RED" cmd /k "node-red"

timeout /t 15 /nobreak > nul

echo [4/4] Iniciando Grafana...
start "Grafana" cmd /k "cd /d ""C:\Program Files\GrafanaLabs\grafana\bin"" && grafana.exe server"

timeout /t 15 /nobreak > nul

echo.
echo ============================================
echo   TODOS LOS SERVICIOS INICIADOS
echo ============================================
echo.

echo InfluxDB  -^>  http://localhost:8086
echo Node-RED  -^>  http://localhost:1880
echo Grafana   -^>  http://localhost:3000
echo MQTT      -^>  localhost:1883

echo.
echo Abriendo navegador...
timeout /t 5 /nobreak > nul

start http://localhost:1880
start http://localhost:3000

pause