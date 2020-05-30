
unused_counter = 0


def clean_name(value):
    global unused_counter
    value = value.replace(" ", "")
    if value == "Unused":
        value = f"Unused_{unused_counter}"
        unused_counter += 1
    else:
        value = value[6:len(value)]
    return value
