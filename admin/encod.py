#imports 
import random
import string
from cryptography.fernet import Fernet

def creating_salt():

    # creating key/salt
    key = Fernet.generate_key().decode()

    # create 3 random strings
    characters = string.ascii_letters
    fake = ''.join(random.choice(characters) for i in range(16))

    # hide salt betweeen fake strings
    salt = fake+key
    return salt

# cleaning salt to original value
def reversing_salt(key):
    salt = key[16:]
    return salt

# function for encryption
def encrypt_data(key, input):
    cipher = Fernet(key.encode())
    data = input.encode()
    cipher_text = cipher.encrypt(data).decode()
    return cipher_text

# function for decryption
def decrypt_data(key, input):
    cipher = Fernet(key.encode())
    decrypted = cipher.decrypt(input).decode()
    return decrypted

