import secrets


def generate_code():
    return secrets.randbelow(900000) + 100000
