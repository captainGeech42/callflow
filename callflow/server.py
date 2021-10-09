import json
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from model import Binary
from db import CallflowDb

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

def import_data(data: str) -> bool:
    b = Binary.from_json(json.loads(data))
    print(b)
    db = CallflowDb("bolt://localhost:7687", "neo4j", "password")
    print(db.add_binary(b))
    db.close()

    return True

with SimpleXMLRPCServer(("0.0.0.0", 8300), requestHandler=RequestHandler, allow_none=True) as server:
   server.register_introspection_functions()
   server.register_function(import_data)
   server.serve_forever()