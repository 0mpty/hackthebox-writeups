from Crypto.Cipher import Salsa20

key = b"ef39f4f20e76e33bd25f4db338e81b10"
nonce = b"d4c270a3"

text = "05055fb1a329a8d558d9f556a6cb31f3" + "24432a31c99dec72e33eb66f62ad1bf9"

text_bytes = bytes.fromhex(text)

cipher_enc = Salsa20.new(key=key, nonce=nonce)
cipher_bytes = cipher_enc.encrypt(text_bytes)
cipher_hex = cipher_bytes.hex()

cipher_dec = Salsa20.new(key=key, nonce=nonce)
decode = cipher_dec.decrypt(bytes.fromhex(cipher_hex))

print(cipher_bytes.decode('utf-8'))
