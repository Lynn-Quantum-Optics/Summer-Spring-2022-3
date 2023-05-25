
command_response_dict = {
    "in": [
        ("ELL", 2),
        ("SN", 8),
        ("YEAR", 4),
        ("FW Rel", 2),
        ("HW Rel", 2),
        ("TRAVEL", 4),
        ("PULSES", 8),
    ],
    "GS": [
        ("STATUS", 2)
    ],
    "I1": [
        ("LOOP", 1),
        ("Motor", 1),
        ("CURRENT", 4),
        ("RAMP UP", 4),
        ("RAMP DOWN", 4),
        ("FORWARD PERIOD", 4),
        ("BACKWARD PERIOD", 4),
    ],
    "PO": [
        ("POSITION", 8)  # Position is returned as a 32 bit signed (2's complement) datatype
    ],
    "HO": [
        ("OFFSET DISTANCE", 8)
    ],
    "GV": [
        ("VELOCITY", 2)  # as a percentage to the nearest integer
    ]
}


def parse_elliptec_response(response_bytes):
    response_dict = {
        "address": response_bytes[0],
        "code": (response_bytes[1:3]).decode()
    }
    index = 3
    for name, num_bytes in command_response_dict[response_dict["code"]]:
        if num_bytes > 1:
            response_dict[name] = int.from_bytes(response_bytes[index:index + num_bytes], 'big')
        else:
            response_dict[name] = response_bytes[index]
        index += num_bytes

    return response_dict
