from typing import Dict, List

class Call:
    def __init__(self, src_va: str, dst_va: str, dst_sym: str):
        self.src_va = src_va
        self.dst_va = dst_va
        self.dst_sym = dst_sym

        self.id = -1

    def set_id(self, id):
        self.id = id

    def to_json(self) -> Dict:
        return {
            "src_va": self.src_va,
            "dst_va": self.dst_va,
            "dst_sym": self.dst_sym
        }
    
    @staticmethod
    def from_json(data):
        c = Call(data["src_va"], data["dst_va"], data["dst_sym"])
        return c

    def __repr__(self):
        return f"<Call {self.src_va} -> {self.dst_sym if len(self.dst_sym) > 0 else self.dst_va}>"

class Function:
    def __init__(self, name: str, va: str, extern: bool):
        self.name = name
        self.va = va
        self.extern = extern

        self.calls: List[Call] = []

        self.id = -1

    def set_id(self, id):
        self.id = id

    def add_call(self, call: Call):
        self.calls.append(call)
    
    def to_json(self) -> Dict:
        return {
            "name": self.name,
            "va": self.va,
            "extern": self.extern,
            "calls": [c.to_json() for c in self.calls]
        }
    
    @staticmethod
    def from_json(data):
        f = Function(data["name"], data["va"], data["extern"])
        f.calls = [Call.from_json(x) for x in data["calls"]]
        return f

    def __repr__(self):
        return f"<Function {self.name} @ {self.va} {' (extern)' if self.extern else ''}>"

class Binary:
    def __init__(self, name: str, md5: str, src: str):
        self.name = name
        self.md5 = md5 
        self.src = src

        self.functions: List[Function] = []

        self.id = -1

    def set_id(self, id):
        self.id = id

    def add_func(self, func: Function):
        self.functions.append(func)

    def to_json(self) -> Dict:
        return {
            "name": self.name,
            "md5": self.md5,
            "src": self.src,
            "functions": [f.to_json() for f in self.functions]
        }
    
    @staticmethod
    def from_json(data):
        b = Binary(data["name"], data["md5"], data["src"])
        b.functions = [Function.from_json(x) for x in data["functions"]]
        return b
    
    def __repr__(self):
        return f"<Binary {self.name} ({self.md5[:6]}...) from {self.src}>"