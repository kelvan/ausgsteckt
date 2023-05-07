import socket

hosts = {
    'fedora': 'production', 'fedora.ist-total.org': 'production',
}
DEFAULT = 'development'

def get_server_type():
    host = socket.gethostname()
    server_type = hosts.get(host, DEFAULT)
    return server_type
