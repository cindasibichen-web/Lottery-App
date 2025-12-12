import base64
import json
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

# 1️⃣ Load Backend Public Key (Flutter would have this)
public_key = RSA.import_key(open("public.pem").read())

# 2️⃣ Generate AES key
aes_key = get_random_bytes(32)  # AES-256

# 3️⃣ Simulate data Flutter sends
data = {
    "name": "John",
    "amount": 500,
    "phone": "9876543210"
}

plaintext = json.dumps(data).encode()

# 4️⃣ AES encryption
cipher_aes = AES.new(aes_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

# 5️⃣ Encrypt AES key using RSA public key
cipher_rsa = PKCS1_OAEP.new(public_key)
enc_aes_key = cipher_rsa.encrypt(aes_key)

# 6️⃣ Construct payload like Flutter sends
payload = {
    "key": base64.b64encode(enc_aes_key).decode(),
    "nonce": base64.b64encode(cipher_aes.nonce).decode(),
    "tag": base64.b64encode(tag).decode(),
    "data": base64.b64encode(ciphertext).decode()
}

print("📤 Payload sent from Flutter simulation:\n", payload)


# ================================
# BACKEND SIDE DECRYPTION
# ================================

# 7️⃣ Load private key
private_key = RSA.import_key(open("private.pem").read())
cipher_rsa = PKCS1_OAEP.new(private_key)

# 8️⃣ Decrypt AES key
aes_key_backend = cipher_rsa.decrypt(base64.b64decode(payload["key"]))

# 9️⃣ Decrypt data
cipher_aes = AES.new(aes_key_backend, AES.MODE_EAX, nonce=base64.b64decode(payload["nonce"]))
plaintext_backend = cipher_aes.decrypt_and_verify(
    base64.b64decode(payload["data"]),
    base64.b64decode(payload["tag"])
)

print("\n🔓 Backend decrypted data:")
print(json.loads(plaintext_backend))
