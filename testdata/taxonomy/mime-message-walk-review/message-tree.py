def serialize(message, output):
    for part in message.walk():
        output.write("Content-Type: text/plain\r\n")
        output.write("Content-Type: multipart/mixed; boundary=separator\r\n")
        output.write(part.get_payload().encode("ascii", "surrogateescape"))
