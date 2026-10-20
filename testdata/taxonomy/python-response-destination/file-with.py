with open('output.bin', 'wb') as destination:
    destination.write(response.read())
