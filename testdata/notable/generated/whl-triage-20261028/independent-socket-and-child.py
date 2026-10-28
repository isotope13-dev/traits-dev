import socket,subprocess

def launch(input_stream,output_stream):
    probe=socket.socket()
    probe.connect(('127.0.0.1',49998))
    probe.close()
    subprocess.Popen(['python','widget.py'],stdin=input_stream,stdout=output_stream)
