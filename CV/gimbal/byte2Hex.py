import binascii

def decto(value):
    hexnum = hex(value)[2:]
    length = (len(hexnum))
    while length <= 3:
        hexnum = '0' + hexnum
        length = (len(hexnum))
    hexflip = flip(hexnum)
    return hexflip


# Flips HEX bytes, 2 bytes at a time
def flip(bytes):
    format = "".join(reversed([bytes[i:i + 2] for i in range(0, len(bytes), 2)]))
    return format


# snips out param DATA bytes
def snip(snips, start, stop):
    snips = (binascii.b2a_hex(snips).decode("utf-8"))[start:stop]
    return snips
