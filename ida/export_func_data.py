import binascii
import json
from typing import Dict, List
import xmlrpc.client

import idaapi
import idautils
import ida_nalt
import ida_name
import ida_xref

# copied from callflow/model.py
from model import Binary, Function, Call

from typing import List

# https://reverseengineering.stackexchange.com/a/4277
def get_calls_for_function(func: Function):
    for i in idautils.FuncItems(int(func.va, 16)):
        for xref in idautils.XrefsFrom(i, 0):
            if xref.type in [ida_xref.fl_CN, ida_xref.fl_CF]:
                dst_name = ida_name.get_name(xref.to)

                if dst_name[0] == ".":
                    dst_name = dst_name[1:]

                c = Call(hex(i), hex(xref.to), dst_name)
                func.add_call(c)

# https://reverseengineering.stackexchange.com/a/13629
# on linux, this pulls from .dynsym, and maybe others, need to test more
def get_external_func_list() -> Dict[str, str]:
    ext_funcs: Dict[str, str] = {}

    def callback(ea, name, ord):
        if name is not None:
            # TODO: name may be None, figure out what to do with that
            # .dynsym func names are like strcspn@@GLIBC_2.2.5

            # this was causing problems with __cxa_finalize
            # the sym is called __imp__cxa_finalize or something, but ida changes it in the name value
            # ext_funcs[name.split("@@")[0]] = hex(ea)

            ext_funcs[ida_name.get_name(ea)] = hex(ea)

        return True

    num_imps = idaapi.get_import_module_qty()

    for i in range(num_imps):
        name = idaapi.get_import_module_name(i)
        idaapi.enum_import_names(i, callback)

    return ext_funcs

def get_functions() -> List[Function]:
    # get a list of extern funcs
    extern_syms = get_external_func_list()

    funcs = []
    for f in idautils.Functions():
        name = ida_name.get_name(f)

        # external funcs on linux start with a "."
        # this leads to duplicates
        # the code calls the one with a ., that is the plt symbol
        
        # is this function in the extern list?
        if name in extern_syms:
            # if we are here, this is a dup function that we don't care about (va that isn't referenced)
            continue

        if name[0] == ".":
            # if we are here, this is an extern in the plt that actually gets called
            name = name[1:]
            # this is actually a garbage check, i think any func thats starts with a _ might flag this
            # e.g., _init_proc and _term_proc are tripping this detection. probably have to get smart and check segment :(
            if name not in extern_syms:
                print(f"error: {name} should be in extern_syms but is not")
    
        funcs.append(Function(name, hex(f), name in extern_syms))

        if name in extern_syms.keys():
            # remove it from the extern sym list
            # then we can add the ones that are only present there back to the graph
            del extern_syms[name]

    # add the only extern things in
    for sym, va in extern_syms.items():
        funcs.append(Function(sym, va, True))

    return funcs

def main():
    funcs = get_functions()
    for f in funcs:
        get_calls_for_function(f)

    # TODO: handle windows path
    name = ida_nalt.get_input_file_path().split("/")[-1]
    md5 = binascii.hexlify(idautils.GetInputFileMD5()).decode()
    binary = Binary(name, md5, "ida")
    
    binary.functions = funcs
    dump = json.dumps(binary.to_json())

    with open("data.json", "w") as f:
        f.write(dump)

    client = xmlrpc.client.ServerProxy("http://localhost:8300", allow_none=True)
    client.import_data(dump)

    print("exported function data to server")

if __name__ == "__main__":
    main()