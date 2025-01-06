from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

# Encryption Configuration
SALT_SIZE = 16  # bytes
KEY_SIZE = 32  # bytes
ITERATIONS = 1000000 # increase from 100000 to 1 mil to further slow down brute-force attempts

def generate_key(password, salt):
    """Derive a cryptographic key from the password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_content(password, plaintext):
    """
    Encrypts the given plaintext content using a password-derived key.
    Returns the salt, IV, and ciphertext as a single encoded string.
    """
    salt = os.urandom(SALT_SIZE)
    key = generate_key(password, salt)
    
    # Encrypt using AES-GCM for authenticated encryption
    aesgcm = AESGCM(key)
    iv = os.urandom(12)  # 96-bit IV for AES-GCM
    ciphertext = aesgcm.encrypt(iv, plaintext.encode(), None)
    
    # Encode salt, iv, and ciphertext for storage
    encrypted_content = base64.b64encode(salt + iv + ciphertext).decode()
    return encrypted_content

def decrypt_content(password, encrypted_content):
    """
    Decrypts the given encrypted content using a password-derived key.
    Expects the encrypted content to contain the salt, IV, and ciphertext.
    """
    decoded_data = base64.b64decode(encrypted_content.encode())
    salt = decoded_data[:SALT_SIZE]
    iv = decoded_data[SALT_SIZE:SALT_SIZE + 12] 
    ciphertext = decoded_data[SALT_SIZE + 12:]
    
    key = generate_key(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(iv, ciphertext, None).decode()
    return plaintext

# Example usage
password = "user_password"
plaintext_content = "Sensitive data to encrypt and store in the file."

# Encrypt content before writing to file
encrypted_content = encrypt_content(password, plaintext_content)
print("Encrypted content:", encrypted_content)

# Decrypt content after reading from file
decrypted_content = decrypt_content(password, encrypted_content)
print("Decrypted content:", decrypted_content)