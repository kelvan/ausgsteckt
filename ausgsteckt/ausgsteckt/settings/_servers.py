import socket

hosts = {
    'doyle': 'production', 'doyle.ist-total.org': 'production',
    'snowden': 'production', 'snowden.ist-total.org': 'production'
}
DEFAULT = 'development'


def get_server_type():
    host = socket.gethostname()
    return hosts.get(host, DEFAULT)
