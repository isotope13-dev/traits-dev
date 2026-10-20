def quit(connection):
    connection.send("QUIT :Goodbye\r\n")
