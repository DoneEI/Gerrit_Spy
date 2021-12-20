import re


def strIsNotEmpty(string: str):
    return string is not None and not str(string).isspace()


def validTimeStr(string: str):
    if string is not None:
        time_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}($|\d{2}:\d{2}:\d{2})$')
        return time_pattern.match(string)

    return False


def validStatus(string: str):
    valid_status = ['abandoned', 'closed', 'merged', 'open', 'reviewed']
    return string in valid_status
