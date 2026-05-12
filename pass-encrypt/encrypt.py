import os
import hmac
import hashlib
import base64
import string
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        length=32,
        iterations=600000,
    )
    return kdf.derive(master_password.encode("utf-8"))


def generate_salt():
    return os.urandom(32)


def encrypt(data, key):
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data.encode("utf-8"), None)
    return {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
    }


def decrypt(blob, key):
    nonce = base64.b64decode(blob["nonce"])
    ciphertext = base64.b64decode(blob["ciphertext"])
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode("utf-8")
    except Exception:
        raise ValueError("Decryption failed — wrong key or corrupted data.")


def generate_site_password(master_key, site, username, length=20, version=1, use_symbols=True):
    message = f"{site.lower().strip()}|{username.lower().strip()}|{version}".encode()

    digest = hmac.new(master_key, message, hashlib.sha256).digest()

    raw = digest
    while len(raw) < length * 4:
        raw += hmac.new(master_key, raw + message, hashlib.sha256).digest()

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits    = string.digits
    symbols   = "!@#$%^&*()-_=+{}[]:;<>,.?" if use_symbols else ""
    pool      = lowercase + uppercase + digits + symbols

    password_chars = []
    for byte in raw:
        password_chars.append(pool[byte % len(pool)])
        if len(password_chars) >= length:
            break

    required = [lowercase, uppercase, digits]
    if use_symbols:
        required.append(symbols)
    offset = length
    for char_class in required:
        pos  = raw[(offset + 1) % len(raw)] % length
        char = char_class[raw[offset % len(raw)] % len(char_class)]
        password_chars[pos] = char
        offset += 2

    return "".join(password_chars)