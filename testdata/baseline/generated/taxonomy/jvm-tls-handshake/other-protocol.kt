class CustomProtocol {
    fun startHandshake() {}
}
fun negotiate(connection: CustomProtocol) {
    connection.startHandshake()
}
