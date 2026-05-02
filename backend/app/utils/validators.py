import re


PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")


def validate_pan(pan_number: str) -> bool:
    if not pan_number:
        return False
    return bool(PAN_REGEX.fullmatch(pan_number.strip().upper()))