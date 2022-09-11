from cryptography.fernet import Fernet
encrypted = b"...encrypted bytes..."

f = Fernet("137C4D1F316EF8A7")
decrypted = f.decrypt(encrypted)
print(decrypted) 