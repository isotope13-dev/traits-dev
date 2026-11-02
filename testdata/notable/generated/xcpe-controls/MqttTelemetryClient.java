package com.example.sensors;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttMessage;

// Benign control: an ordinary MQTT telemetry client. It subscribes to a
// configuration topic and publishes sensor readings; broker messages only
// adjust a sampling interval. No shell, installs, or screen access.
public class MqttTelemetryClient implements MqttCallback {
    private MqttClient client;
    private int sampleSeconds = 60;

    public void start() throws Exception {
        client = new MqttClient("tcp://mqtt.example.org:1883", "sensor-7");
        client.setCallback(this);
        client.connect();
        client.subscribe("sensors/7/config");
    }

    public void publishReading(double celsius) throws Exception {
        String body = "{\"celsius\":" + celsius + "}";
        client.publish("sensors/7/temperature", body.getBytes(), 0, false);
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) {
        try {
            int value = Integer.parseInt(new String(message.getPayload()).trim());
            if (value >= 5 && value <= 3600) sampleSeconds = value;
        } catch (NumberFormatException ignored) { }
    }

    @Override public void deliveryComplete(IMqttDeliveryToken token) { }
    @Override public void connectionLost(Throwable cause) { }
}
