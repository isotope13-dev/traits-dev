import javax.net.ssl.SSLSocket
fun negotiate(connection: SSLSocket) {
    connection.startHandshake()
}
