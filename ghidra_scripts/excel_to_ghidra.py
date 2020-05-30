#Parse excel spreadsheet and populate function definitions
#@category Automation
#@author Villarreal
 
import json

from ghidra.util.exception import CancelledException, InvalidInputException
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DataTypeConflictHandler
from ghidra.app.util.cparser.C import CParser
from ghidra.program.model.data import CategoryPath


def build_structs(struct_list):
    monitor.setMessage("Creating structures")
    dt_manager = currentProgram.getDataTypeManager()
    parser = CParser(dt_manager)
    category_path = CategoryPath("/D2")
    for struct_name in struct_list:
        monitor.checkCanceled()
        struct_txt = "struct {}".format(struct_name) + "{};"
        parsed_struct = parser.parse(struct_txt)
        try:
            parsed_struct.setCategoryPath(category_path)
        # I think this happens when the struct is already defined.
        except AttributeError:
            continue
        dt_manager.addDataType(parsed_struct, DataTypeConflictHandler.DEFAULT_HANDLER)
    

def build_funcs(funcs_list):
    monitor.setMessage("Syncing functions")
    for func in currentProgram.functionManager.getFunctionsNoStubs(1):
        monitor.checkCanceled()
        if "Ordinal" not in func.name:
            continue
        _, ordinal = func.name.split("_")
        func_entry = lookup_ordinal(ordinal, funcs_list)
        if not func_entry:
            continue
        configure_func(func, func_entry)


def set_func_return_type(ghidra_func, spreadsheet_func):
    dt_manager = currentProgram.getDataTypeManager()
    if spreadsheet_func["return_type"].startswith("D2"):
        return_type = dt_manager.findDataType("/D2/{}".format(spreadsheet_func["return_type"]))
        ghidra_func.setReturnType(return_type, SourceType.USER_DEFINED)
    else:
        # Loop all categories to find the return type.
        pass


def set_func_parameters(ghidra_func, spreadsheet_func):
    pass


def configure_func(ghidra_func, spreadsheet_func):
    print("{} -> {}".format(ghidra_func.name, spreadsheet_func["name"]))
    ghidra_func.setName(spreadsheet_func["name"], SourceType.USER_DEFINED)
    # set_func_return_type(ghidra_func, spreadsheet_func)
    try:
        ghidra_func.setCallingConvention(spreadsheet_func["calling_convention"])
    # Some functions are labled as "int" for calling convention.
    except InvalidInputException:
        pass
    # set_func_parameters(ghidra_func, spreadsheet_func)


def lookup_ordinal(ordinal, funcs_list):
    for entry in funcs_list:
        if entry["ordinal"] == ordinal:
            return entry


def main():
    input_json_file = str(askFile("Select input spreadsheet", "Open"))
    with open(input_json_file) as f:
        spreadsheet = json.load(f)
    print("Syncing excel spreadsheet with ghidra database")
    build_structs(spreadsheet["structs"])
    build_funcs(spreadsheet["functions"])


try:
    main()
except CancelledException:
    pass
