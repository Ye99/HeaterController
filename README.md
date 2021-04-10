# HeaterController
ESP8266 heater controller to maintain certain minimum temperature

Flash credentials.json into your MicroPython root folder, with below content: 
```json
{
  "MQTT": {
    "server": "your MQTT server ip",
    "client_id": "client id",
    "port": 1883,
    "user": "MQTT username",
    "pwd": "MQTT password",
    "topic": "message topic"
  },
  "Wifi": {
    "ssid": "your wifi ssid",
    "pwd": "your wifi password"
  },
  "Comment": "temperature or humidity. If other than these, control function is disabled.",
  "Control_Strategy": "temperature",
  "Location": "where is this controller"
}
```
You will see MQTT message like:
```csv
status,location=printershed-1f,control_strategy=temperature,sequence_id=357 temperature=13.02,humidity=42.1758,pressure=101452,relay=off,relay_off->on=False,relay_on->off=False
```
