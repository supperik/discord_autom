import time


def calculate_nonce() -> str:
    unix_ts = time.time()
    return str((int(unix_ts) * 1000 - 1420070400000) * 4194304)