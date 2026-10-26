fun main() {
    val stores = listOf("/data/misc/keystore", "/data/misc/wifi/wpa_supplicant.conf")
    val request = "POST /exfil HTTP/1.1"
    println(stores.toString() + request)
}
