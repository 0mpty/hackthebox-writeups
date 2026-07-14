import ctypes
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def decrypt_message(encrypted_message, key):
    try:
        key = key.ljust(32, b'\x00')
        iv = encrypted_message[:16]
        ciphertext = encrypted_message[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()
        return decrypted_message.decode()
    except Exception as e:
        return None

def start(key):
    encrypted_message = bytes.fromhex('ad24426047b0ffb03b679773664838462a6f00bdcaf0589dd1748e9ed5c568601edc87d974894f9dd9b98cc35535145c494eb0af84c8f78d440a033c91c7de62d506d8cabdc2a10138b95139bbe60e89')
    decrypted_message = decrypt_message(encrypted_message, key.encode())
    if decrypted_message:
        print(f"Decrypted message: {decrypted_message}")
        return True
    return False



libc = ctypes.CDLL('libc.so.6')

hour = 0
minute = 0
second = 0

character_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_+0123456789"
password_length = 20
length = len(character_set)

while hour < 24:
    my_tm = (2013, 12, 11, hour, minute, second, 2, 345, -1)

    target_time = int(time.mktime(my_tm))
    local_struct = time.localtime(target_time)

    generated_password = ""   

    libc.srand(local_struct.tm_mday * 1000000 + local_struct.tm_min * 100 + local_struct.tm_sec + local_struct.tm_hour * 10000 + 
               (local_struct.tm_year - 1900 + 0x76c) * 0x540be400 + local_struct.tm_mon * 100000000)

    for _ in range(password_length):
        random_index = libc.rand() % length
        generated_password += character_set[random_index]  
    
    result = start(generated_password)

    print(f"{hour}:{minute}:{second} : {generated_password}")

    if result: 
        break

    second += 1

    if (second == 60):
        minute += 1
        second = 0
    if (minute == 60):
        hour += 1
        minute = 0

print("End")
