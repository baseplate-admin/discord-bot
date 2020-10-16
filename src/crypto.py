import os
from cryptography.fernet import Fernet

cipher = Fernet("T7OARaKJbKUmmbNfKIppYoI88mamK7WSdK88qyJqlfg=")
def encrypt(file):
    with open(file, "rb") as f:
        content = f.read()
    encryption = cipher.encrypt(content)
    for files in os.listdir("./"):
        if files.endswith(".json"):
            with open(file[0:-5] + ".ejson", "wb") as f:
                f.write(encryption)
    if file.endswith('.json'):
        os.remove(file)
    elif file.endswith('.txt'):
        os.remove(file)
def decrypt(file):
    with open(file, "rb") as f:
        content = f.read()
    decryption = cipher.decrypt(content)
    for files in os.listdir("./"):
        if files.endswith(".ejson"):
            with open(file[0:-6] + ".json", "wb") as f:
                f.write(decryption)

    if file.endswith(".ejson"):
        os.remove(file)
    elif file.endswith(".etxt"):
        os.remove(file)
