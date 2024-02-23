import random
import string

import loguru


def generate_random_session_id() -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


def generate_random_time(account_index):
    rtime = int(random.random() * 86400)
    hours = int(rtime / 3600)
    minutes = int((rtime - hours * 3600) / 60)
    seconds = rtime - hours * 3600 - minutes * 60
    time_string = '%02d:%02d:%02d' % (hours, minutes, seconds)
    loguru.logger.info(f"Button will press again for account {account_index} in {time_string}")
    return time_string
