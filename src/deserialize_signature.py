def _extract_return_type(signature):
    return signature.split(" ")[0]


def _extract_calling_convention(signature):
    return signature.split(" ")[1]


def _extract_parameters(signature):
    # TODO: this doesn't handle nested parenthesis:
    # void __stdcall MONSTERS_GetMinionSpawnInfo(D2UnitStrc* pMonster, int* pId, int* pX, int* pY, int* a5, int nBaseChainId, int(__fastcall* pfSpawnClassCallback)(D2UnitStrc*));
    parameter_string = signature[signature.find("(") + 1:signature.find(")")]
    if not parameter_string:
        return []
    parameter_list = parameter_string.split(", ")
    return parameter_list


def deserialize_signature(signature):
    return {
        "return_type": _extract_return_type(signature),
        "calling_convention": _extract_calling_convention(signature),
        "parameters": _extract_parameters(signature),
    }
