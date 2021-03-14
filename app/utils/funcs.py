import time


def delta_time(start: float):
    return round((time.time() - start) * 1000)
