from proton.utils import BlockingConnection

def notify(url, target, message):
    connection = BlockingConnection(url)
    sender = connection.create_sender(target)
    sender.send(message)
