import random
import string


def generate_random_session_id() -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


def generate_random_time():
    rtime = int(random.random() * 86400)
    hours = int(rtime / 3600)
    minutes = int((rtime - hours * 3600) / 60)
    seconds = rtime - hours * 3600 - minutes * 60
    time_string = '%02d:%02d:%02d' % (hours, minutes, seconds)
    return time_string
