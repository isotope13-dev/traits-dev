fun main() {
    val stores = listOf("/data/misc/keystore", "/data/misc/wifi/wpa_supplicant.conf")
    val header = "Content-Type: application/octet-stream"
    println(stores.toString() + header)
}
