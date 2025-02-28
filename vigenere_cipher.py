def vigenere_encrypt(plain, key):
    plain_text = plain.lower() #supprimer les espaces
    
    # preparer la clé
    extended_key=""
    key_index = 0
    for char in plain_text:
        if char.isalpha():
            extended_key += key[key_index % len(key)]
            key_index += 1
        else:
            extended_key += ' '
    
    result = ''
    for i,char in enumerate(plain_text):
        if char.isalpha():
            key_char = extended_key[i]
            key_shift = ord(key_char) - ord('a')
            
            shifted = (ord(char) - ord('a') + key_shift) % 26 + ord('a')
            result += chr(shifted)
        else:
            result += ' '
    
    return result
        
def vigenere_decrypt(cipher, key):
    cipher_text = cipher.lower() #supprimer les espaces
    
    # preparer la clé
    extended_key=""
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            extended_key += key[key_index % len(key)]
            key_index += 1
        else:
            extended_key += ' '
    
    result = ''
    for i,char in enumerate(cipher_text):
        if char.isalpha():
            key_char = extended_key[i]
            key_shift = ord(key_char) - ord('a')
            
            shifted = (ord(char) - ord('a') - key_shift) % 26 + ord('a')
            result += chr(shifted)
        else:
            result += ' '
    
    return result

encrypted = vigenere_encrypt("lina is amazing","bet")
print(encrypted)
decrypted = vigenere_decrypt(encrypted,"bet")
print(decrypted)