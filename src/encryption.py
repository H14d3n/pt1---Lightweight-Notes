import base64
import os
import random
import secrets
import string

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


PASSWORD_PREFIX = "scrypt$v1"
NOTE_PREFIX = "enc$aesgcm$v1"

_PASSWORD_SALT_BYTES = 16
_PASSWORD_KEY_BYTES = 32
_NOTE_SALT_BYTES = 16
_NOTE_NONCE_BYTES = 12

# Scrypt parameters chosen to be strong enough for desktop apps while keeping login responsive.
_SCRYPT_N = 2**14
_SCRYPT_R = 8
_SCRYPT_P = 1


def _derive_scrypt_key(secret: str, salt: bytes, length: int) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=length,
        n=_SCRYPT_N,
        r=_SCRYPT_R,
        p=_SCRYPT_P,
    )
    return kdf.derive(secret.encode("utf-8"))


def hash_password(password: str) -> str:
    """Hash a password with scrypt and return a self-contained encoded string."""
    salt = os.urandom(_PASSWORD_SALT_BYTES)
    digest = _derive_scrypt_key(password, salt, _PASSWORD_KEY_BYTES)
    return f"{PASSWORD_PREFIX}${base64.b64encode(salt).decode('ascii')}${base64.b64encode(digest).decode('ascii')}"


def is_password_hashed(stored_password: str) -> bool:
    return isinstance(stored_password, str) and stored_password.startswith(f"{PASSWORD_PREFIX}$")


def verify_password(password: str, stored_password: str) -> bool:
    """Verify current scrypt hashes and transparently support legacy plaintext rows."""
    if not stored_password:
        return False

    if not is_password_hashed(stored_password):
        return secrets.compare_digest(password, stored_password)

    parts = stored_password.split("$")
    if len(parts) != 4:
        return False

    try:
        salt = base64.b64decode(parts[2])
        expected = base64.b64decode(parts[3])
    except Exception:
        return False

    candidate = _derive_scrypt_key(password, salt, len(expected))
    return secrets.compare_digest(candidate, expected)


def encrypt_document_text(plain_text: str, password: str) -> str:
    """Encrypt note body (lines 3+) with AES-GCM and keep metadata lines unchanged."""
    lines = plain_text.splitlines()
    header = lines[:2]
    body = "\n".join(lines[2:])

    salt = os.urandom(_NOTE_SALT_BYTES)
    nonce = os.urandom(_NOTE_NONCE_BYTES)
    key = _derive_scrypt_key(password, salt, _PASSWORD_KEY_BYTES)
    ciphertext = AESGCM(key).encrypt(nonce, body.encode("utf-8"), None)

    payload = "|".join(
        [
            NOTE_PREFIX,
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(nonce).decode("ascii"),
            base64.b64encode(ciphertext).decode("ascii"),
        ]
    )

    return "\n".join(header + [payload]) + "\n"


def decrypt_document_text(content: str, password: str, uid=None) -> str:
    """Decrypt AES-GCM notes, or fall back to legacy substitution cipher for old files."""
    lines = content.splitlines()
    if len(lines) < 3:
        return content

    payload_line = lines[2]
    if payload_line.startswith(NOTE_PREFIX + "|"):
        parts = payload_line.split("|")
        if len(parts) != 4:
            raise ValueError("Corrupted encrypted document payload.")

        try:
            salt = base64.b64decode(parts[1])
            nonce = base64.b64decode(parts[2])
            ciphertext = base64.b64decode(parts[3])
            key = _derive_scrypt_key(password, salt, _PASSWORD_KEY_BYTES)
            decrypted = AESGCM(key).decrypt(nonce, ciphertext, None).decode("utf-8")
        except Exception as exc:
            raise ValueError("Unable to decrypt document. Wrong password or corrupted file.") from exc

        return "\n".join(lines[:2] + [decrypted]) + "\n"

    return _decrypt_legacy_document(content, uid)


def _decrypt_legacy_document(content: str, uid) -> str:
    """Legacy compatibility for old deterministic substitution-encrypted documents."""
    if uid is None:
        return content

    try:
        uid_num = int(uid)
    except (TypeError, ValueError):
        return content

    lines = content.splitlines()
    encrypted_body = "\n".join(lines[2:])
    seed = 5901 * uid_num
    chars, key = _generate_legacy_key(seed)
    decrypted_body = _legacy_substitute(encrypted_body, key, chars)
    return "\n".join(lines[:2] + [decrypted_body]) + "\n"


def _generate_legacy_key(seed=None):
    chars = " " + string.punctuation + string.digits + string.ascii_letters
    chars = list(chars)
    random.seed(seed)
    key = chars.copy()
    random.shuffle(key)
    return chars, key


def _legacy_substitute(text, source_chars, target_chars):
    out = []
    for letter in text:
        if letter in source_chars:
            out.append(target_chars[source_chars.index(letter)])
        else:
            out.append(letter)
    return "".join(out)
