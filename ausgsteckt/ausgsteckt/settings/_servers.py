import socket

hosts = {}
DEFAULT = 'development'


def get_server_type():
    host = socket.gethostname()
    return hosts.get(host, DEFAULT)
