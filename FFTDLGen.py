IO_SENSOR_DATA = 5

SENSOR_RANGE_ACC_G = 4      # unit: g
SENSOR_RANGE_ACC_MS = 5     # unit: m/s^2

FFT_X_IDX = 1
FFT_Y_IDX = 2
FFT_Z_IDX = 4

DATA_IDX_LOGIDX_UTC = 11
DATA_IDX_LOGIDX_UTC_LEN = 9


def __crc8(data: bytes, initial_value: int = 0xFF) -> bytes:
    crc = initial_value
    polynomial = 0x07  # CRC-8-CCITT polynomial

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ polynomial) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc.to_bytes(1)

def genFFTDL_logIdx_utc(fcnt: int, log_index: int, timestamp: int, isX: bool = True, isY: bool = True, isZ: bool = True):
    fcnt_b = (fcnt % 256).to_bytes(1)
    header = b''.join([b'\x80', fcnt_b, b'\x0C'])

    log_index = log_index if log_index != 0 else 4294967295
    content = b''.join([
        (IO_SENSOR_DATA << 4 | SENSOR_RANGE_ACC_G).to_bytes(1),
        (FFT_X_IDX << 5 | FFT_Y_IDX << 5 | FFT_Z_IDX << 5).to_bytes(1),
        (DATA_IDX_LOGIDX_UTC_LEN).to_bytes(1),
        (DATA_IDX_LOGIDX_UTC).to_bytes(1),
        log_index.to_bytes(4, 'little'),
        timestamp.to_bytes(4, 'little')
    ])

    crc = __crc8(content)
    ret = header + content + crc

    return ret.hex()

if __name__ == "__main__":
    seq = 0
    log_index = 55
    timestamp = 1729841700
    print(genFFTDL_logIdx_utc(seq, log_index, timestamp))

# 80000C54E0090BFFFFFFFF641F06678D
