# HeaterController
ESP8266 heater controller to maintain certain minimum temperature

Flash credentials.json into your MicroPython root folder, with below content: 
```json
{
  "MQTT": {
    "server": "your MQTT server ip",
    "client_id": "client id",
    "user": "MQTT username",
    "pwd": "MQTT password",
    "topic": "message topic"
  },
  "Wifi": {
    "ssid": "your wifi ssid",
    "pwd": "your wifi password"
  }
}
```