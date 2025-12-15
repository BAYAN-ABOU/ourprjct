import zlib

# =========================
# Parity Bit (Even)
# =========================
def parity_bit(data):
    ones = sum(bin(ord(c)).count("1") for c in data)
    return str(ones % 2)

# =========================
# CRC16
# =========================
def crc16(data):
    crc = zlib.crc32(data.encode()) & 0xFFFF
    return format(crc, '04X')

# =========================
# Internet Checksum
# =========================
def internet_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        word = ord(data[i]) << 8
        if i + 1 < len(data):
            word += ord(data[i+1])
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    return hex(~checksum & 0xFFFF)

# =========================
# Packet Builder
# =========================
def build_packet(data, method="CRC16"):
    if method == "PARITY":
        control = parity_bit(data)
    elif method == "CRC16":
        control = crc16(data)
    elif method == "CHECKSUM":
        control = internet_checksum(data)
    else:
        control = "NULL"

    return f"{data}|{method}|{control}"