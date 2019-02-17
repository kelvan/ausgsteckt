import socket

hosts = {
    'doyle': 'production', 'fedora': 'production', 'fedora.ist-total.org': 'production',
}
DEFAULT = 'development'


def get_server_type():
    host = socket.gethostname()
    return hosts.get(host, DEFAULT)
