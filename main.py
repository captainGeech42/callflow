import json
import traceback

from callflow.db import CallflowDb
from callflow.model import Binary, Function, Call

from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

def import_data(data: str):
    b = Binary.from_json(json.loads(data))
    print(b)
    db = CallflowDb("bolt://localhost:7687", "neo4j", "password")
    try:
        print(db.add_binary(b))
    except:
        traceback.print_exc()
    db.close()

with SimpleXMLRPCServer(("0.0.0.0", 8300), requestHandler=RequestHandler, allow_none=True, logRequests=False) as server:
   server.register_introspection_functions()
   server.register_function(import_data)
   server.serve_forever()
   
# if __name__ == "__main__":
    # db = CallflowDb("bolt://localhost:7687", "neo4j", "password")

    # func1 = Function("main", "0x401030")
    # func1.add_call(Call("0x401048", "0x401269", "print_name"))

    # func2 = Function("print_name", "0x401269")

    # binary = Binary("pwn1", "mysha256str", "ida")
    # binary.add_func(func1)
    # binary.add_func(func2)

    # print(db.add_binary(binary))

    # print(binary.functions[0].id)

    # with open("data.json", "r") as f:
    #     data = f.read()

    # bin = Binary.from_json(json.loads(data))
    # print(db.add_binary(bin))

    # db.close()