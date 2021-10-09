from neo4j import GraphDatabase

from .model import Binary, Function, Call

# https://neo4j.com/developer/python/
class CallflowDb:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def add_binary(self, binary: Binary) -> int:
        with self.driver.session() as s:
            binary_id = s.write_transaction(self._create_and_return_binary, binary)
            return binary_id
    
    @staticmethod
    def _create_and_return_binary(tx, binary: Binary) -> int:
        # make the binary node
        result = tx.run("CREATE (b:Binary {name: $name, sha256: $sha256, src: $src}) "
                        "RETURN id(b)",
                        name = binary.name,
                        sha256 = binary.sha256,
                        src = binary.src)
        
        binary_id = result.single()[0]
        binary.set_id(binary_id)

        # add the functions
        for func in binary.functions:
            id = CallflowDb._create_and_return_function(tx, binary, func)
            func.set_id(id)
        
        # add the call edges
        for func in binary.functions:
            for call in func.calls:
                id = CallflowDb._create_and_return_call(tx, binary, func, call)
                call.set_id(id)

        return binary_id

    @staticmethod
    def _create_and_return_function(tx, binary: Binary, func: Function) -> int:
        assert(binary.id != -1)

        # add the edge
        result = tx.run("MATCH (b:Binary) WHERE id(b) = $bin_id "
                        "CREATE (b)-[rel:CONTAINS_FUNCTION]->(f:Function {name: $name, va: $va}) "
                        "RETURN id(f)",
                        name = func.name,
                        va = func.va,
                        bin_id = binary.id)
        
        return result.single()[0]
    
    @staticmethod
    def _create_and_return_call(tx, binary: Binary, func: Function, call: Call) -> int:
        assert(binary.id != -1)
        assert(func.id != -1)

        # TODO: handle case where symbol doesn't exist, or when symbol + va doesn't exist
        result = tx.run("MATCH (b:Binary) WHERE id(b) = $bin_id "
                        "MATCH (src:Function) WHERE id(src) = $func_id "
                        "MATCH (dst:Function {name: $dst_sym}) "
                        "CREATE (src)-[rel:CALLS {src_va: $src_va}]->(dst) "
                        "RETURN id(rel)",
                        bin_id = binary.id,
                        func_id = func.id,
                        dst_sym = call.dst_sym,
                        src_va = call.src_va)
        
        return result.single()[0]
