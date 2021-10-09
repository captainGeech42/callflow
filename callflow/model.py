from typing import List

class Call:
    def __init__(self, src_va: str, dst_va: str, dst_sym: str):
        self.src_va = src_va
        self.dst_va = dst_va
        self.dst_sym = dst_sym

        self.id = -1

    def set_id(self, id):
        self.id = id

    def __repr__(self):
        return f"<Call {self.src_va} -> {self.dst_sym if len(self.dst_sym > 0) else self.dst_va}>"

class Function:
    def __init__(self, name: str, va: str):
        self.name = name
        self.va = va

        self.calls: List[Call] = []

        self.id = -1

    def set_id(self, id):
        self.id = id

    def add_call(self, call: Call):
        self.calls.append(call)

    def __repr__(self):
        return f"<Function {self.name} @ {self.va}>"

class Binary:
    def __init__(self, name: str, sha256: str, src: str):
        self.name = name
        self.sha256 = sha256
        self.src = src

        self.functions: List[Function] = []

        self.id = -1

    def set_id(self, id):
        self.id = id

    def add_func(self, func: Function):
        self.functions.append(func)

    def __repr__(self):
        return f"<Binary {self.name} ({self.sha256[:6]}...) from {self.src}>"