import re


def is_valid(number):
    # 1) Begins with 0 or 91
    # 2) Then contains 6, 7, 8 or 9.
    # 3) Then contains 9 digits
    pattern = re.compile("(91)?[6-9][0-9]{9}")
    return pattern.match(number)


