import os

def send_message(url_pipe, message):
    """sends a message over FIFO. (blocks until the other end reads the message)"""
    fd = os.open(url_pipe, os.O_WRONLY)
    os.write(fd, bytes(message))
    os.close(fd)

def read_message(url_pipe):
    """reads a message from FIFO"""
    fd = os.open(url_pipe, os.O_RDONLY)
    data = os.read(fd, 200)
    if not data:
        os.close(fd)
        return None
    os.close(fd)
    return data