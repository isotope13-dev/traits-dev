from pathlib import Path

def send_files(client):
    virtual_files = client.VirtualStreamSender.RegisterVirtualFiles([b'file'], None)
    message = ScreenConnect.TransferFilesMessage()
    message.Files = virtual_files
    message.Action = ScreenConnect.FileAction.Run
    client.EnqueueOutgoingMessage(message)
# Ordinary operator-invoked transfer API example, with padding to exercise
# the same file-size scope as a complete client implementation. No endpoint
# status handler, Host selection, membership cache, or automatic delivery.
