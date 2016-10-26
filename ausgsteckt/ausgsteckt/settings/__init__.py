from ._servers import get_server_type

exec("from .%s import *" % get_server_type())
