import java.security.MessageDigest
fun fingerprint(data: ByteArray) = MessageDigest.getInstance("SHA-256").digest(data)
