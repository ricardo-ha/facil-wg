from hashlib import sha256

def set_password(password:str):
    return sha256(password.encode("utf-8")).hexdigest()
