import random
import string

def generate_key(seed=None):
    """
    Generates a key based on a fixed seed. If no seed is provided, a default seed is used.
    """
    chars = " " + string.punctuation + string.digits + string.ascii_letters
    chars = list(chars)

    # Use the seed for the random number generator
    random.seed(seed)  # If no seed is provided, the default seed is used
    key = chars.copy()
    random.shuffle(key)

    return chars, key

def encrypt_message(plain_text, chars, key):
    """
    Encrypts the message using the provided key.
    """
    cipher_text = ""
    
    for letter in plain_text:
        if letter in chars:
            index = chars.index(letter)
            cipher_text += key[index]
        else:
            cipher_text += letter  # If the character is not in the chars list, leave it unchanged

    return cipher_text

def decrypt_message(encrypted_text, chars, key):
    """
    Decrypts the message using the provided key by reversing the encryption process.
    """
    decrypted_text = ""
    
    for letter in encrypted_text:
        if letter in key:
            index = key.index(letter)
            decrypted_text += chars[index]
        else:
            decrypted_text += letter  # If the character is not in the key list, leave it unchanged

    return decrypted_text
