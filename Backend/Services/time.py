import datetime

def to_ddmmYYYY_str(time:datetime) -> str:
    return time.strftime('%d/%m/%Y')

def to_HHMMSS_ddmmYYYY_str(time:datetime) -> str:
    return time.strftime('%H:%M:%S %d/%m/%Y')