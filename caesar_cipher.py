def caesar_encrypt(plain, key):
    plain_text = plain.lower().strip()
    try:
        key = int(key)  # on essaie de rendre la clé en un entier, si c'est pas possible alors ce n'est pas un nombre
    except ValueError:
        print("the key has to be a number")
        return
    
    result = ""
    for char in plain_text:
        if char.isalpha():
            shifted = (ord(char) - ord('a') + key) % 26 + ord('a') # on considere seulement les lettres minuscules (26 lettres), et comme on utilise mod 26 on diminue l'ascii de a pour retomber dans ces valeurs entre 0 et 25
            result += chr(shifted)
        else:
            result += char
    return result



def caesar_decrypt(cipher,key):
    cipher_text = cipher.lower().strip()
    try:
        key = int(key)
    except ValueError:
        print("key is not a number")
        return

    result = ""
    for char in cipher_text:
        if char.isalpha():
            shifted = (ord(char) - ord('a') - key) % 26 + ord('a')
            result += chr(shifted)
        else:
            result += char
    return result

encrypted = caesar_encrypt('lina is amazing', 20)
print(encrypted)
decrypted = caesar_decrypt(encrypted,20)
print(decrypted)