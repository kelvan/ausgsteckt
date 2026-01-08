import socket

from .conf import DjangoConfig

hosts = {
    "ausgsteckt": "production",
    "ausgsteckt.ist-total.org": "production",
}
DEFAULT = "development"


def get_server_type():
    config = DjangoConfig()
    if config.server_type:
        return config.server_type
    host = socket.gethostname()
    server_type = hosts.get(host, DEFAULT)
    return server_type
