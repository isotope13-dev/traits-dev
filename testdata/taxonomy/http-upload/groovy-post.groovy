def conn = new URL('https://example.invalid/upload').openConnection()
conn.setRequestMethod('POST')
conn.outputStream.write('status'.bytes)
