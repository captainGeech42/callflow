import json
import traceback
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from .model import Binary
from .db import CallflowDb

# https://www.tutorialspoint.com/xmlrpc-server-and-client-modules-in-python

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

class CallflowServer:
    def __init__(self, host: str, port: int, db: CallflowDb):
        self.host = host
        self.port = port
        self.db = db

    def run(self):
        def import_data(data: str):
            print("importing data...")
            b = Binary.from_json(json.loads(data))
            print(f"successful import, adding to db: {b}")
            try:
                id = self.db.add_binary(b)
                print(f"added to db, binary id is {id}")
            except:
                print("failed to add to db")
                traceback.print_exc()

        with SimpleXMLRPCServer((self.host, self.port), requestHandler=RequestHandler, allow_none=True, logRequests=False) as server:
            server.register_introspection_functions()
            server.register_function(import_data)

            print(f"listening on {self.host}:{self.port}...")
            server.serve_forever()