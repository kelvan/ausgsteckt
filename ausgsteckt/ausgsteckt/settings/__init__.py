from ._servers import get_server_type

exec(f"from .{get_server_type()} import *")
