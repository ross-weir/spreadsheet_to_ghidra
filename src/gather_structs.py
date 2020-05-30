def strip_type(value):
    value = value.replace("*", "")
    value = value.replace(" ", "")
    return value


def gather_structs_from_entries(entries):
    structs = []
    for entry in entries:
        return_type = strip_type(entry["return_type"])
        if return_type not in structs and return_type.startswith("D2"):
            structs.append(return_type)
        for param in entry["parameters"]:
            stripped_param = strip_type(param)
            if stripped_param not in structs and stripped_param.startswith("D2"):
                structs.append(stripped_param)
    return structs
