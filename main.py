from callflow.db import CallflowDb
from callflow.model import Binary, Function, Call

if __name__ == "__main__":
    db = CallflowDb("bolt://localhost:7687", "neo4j", "password")

    func1 = Function("main", "0x401030")
    func1.add_call(Call("0x401048", "0x401269", "print_name"))

    func2 = Function("print_name", "0x401269")

    binary = Binary("pwn1", "mysha256str", "ida")
    binary.add_func(func1)
    binary.add_func(func2)

    print(db.add_binary(binary))

    print(binary.functions[0].id)

    db.close()