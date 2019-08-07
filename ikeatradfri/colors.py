hex_colors = {
    0: {"Name": "Blue", "Hex": "4a418a"},
    10: {"Name": "Candlelight", "Hex": "ebb63e"},
    20: {"Name": "Cold sky", "Hex": "dcf0f8"},
    30: {"Name": "Cool daylight", "Hex": "eaf6fb"},
    40: {"Name": "Cool white", "Hex": "f5faf6"},
    50: {"Name": "Dark Peach", "Hex": "da5d41"},
    60: {"Name": "Light Blue", "Hex": "6c83ba"},
    70: {"Name": "Light Pink", "Hex": "e8bedd"},
    80: {"Name": "Light Purple", "Hex": "c984bb"},
    90: {"Name": "Lime", "Hex": "a9d62b"},
    100: {"Name": "Peach", "Hex": "e57345"},
    110: {"Name": "Pink", "Hex": "e491af"},
    120: {"Name": "Saturated Red", "Hex": "dc4b31"},
    130: {"Name": "Saturated Pink", "Hex": "d9337c"},
    140: {"Name": "Saturated Purple", "Hex": "8f2686"},
    150: {"Name": "Sunrise", "Hex": "f2eccf"},
    160: {"Name": "Yellow", "Hex": "d6e44b"},
    170: {"Name": "Warm Amber", "Hex": "e78834"},
    180: {"Name": "Warm glow", "Hex": "efd275"},
    190: {"Name": "Warm white", "Hex": "f1e0b5"},
}

hex_whites = {
    0: {"Name": "Cold", "Hex": "f5faf6"},
    10: {"Name": "Normal", "Hex": "f1e0b5"},
    20: {"Name": "Warm", "Hex": "efd275"},
}

def list_hexes(colorspace, levels=False):
    retVal = ""
    target = ""
    target = hex_colors if colorspace == "CWS" else hex_whites

    for key, aColor in sorted(target.items()):
        if not levels:
            retVal = "{0}{1} : {2}\n".format(retVal, aColor["Hex"], aColor["Name"])
        else:
            retVal = "{0}{1} : {2}\n".format(retVal, key, aColor["Name"])

    return retVal[:-1]

def color(level, colorspace="WS"):
    return hex_colors[int(level)] if colorspace == "CWS" else hex_whites[int(level)]
    
def color_level_definitions(colorspace):
    levels=""
    actions=""
    target = hex_colors if colorspace == "CWS" else hex_whites

    for _, aColor in sorted(target.items()):
        levels="{0}{1}|".format(levels, aColor["Name"])
        actions="{0}{1}|".format(actions, "")

    return levels[:-1], actions[:-1]

def color_level_for_hex(hex, colorspace):
    target = hex_colors if colorspace == "CWS" else hex_whites

    for key in target:
        if target[key]["Hex"] == hex:
            return key

def color_name_for_hex(hex, colorspace):
    target = hex_colors if colorspace == "CWS" else hex_whites
    
    
    return target[color_level_for_hex(hex, colorspace)]["Name"]


