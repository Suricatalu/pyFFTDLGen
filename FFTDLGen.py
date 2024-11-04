import DownlinkGenHdr as DWHDR

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
        (DWHDR.IO_SENSOR_DATA << 4 | DWHDR.SENSOR_RANGE_ACC_G).to_bytes(1),
        (DWHDR.FFT_X_IDX << 5 | DWHDR.FFT_Y_IDX << 5 | DWHDR.FFT_Z_IDX << 5).to_bytes(1),
        (DWHDR.DATA_IDX_LOGIDX_UTC_LEN).to_bytes(1),
        (DWHDR.DATA_IDX_LOGIDX_UTC).to_bytes(1),
        log_index.to_bytes(DWHDR.PARA_LOGIDX_SIZE, 'little'),
        timestamp.to_bytes(DWHDR.PARA_TIME_SIZE, 'little')
    ])

    crc = __crc8(content)
    ret = header + content + crc

    return ret.hex()

if __name__ == "__main__":
    seq = 0
    log_index = 55
    timestamp = 1729841700
    print(genFFTDL_logIdx_utc(seq, log_index, timestamp))

# Output: 80000c54e0090b37000000244a1b6765
