import math

# class exception pour gérer le cas ou a n'est pas premier avec 26
class NotCoprimeError(Exception):
    pass


def affine_encrypt(plain, a, b):
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        print("NUMBERS PLEASE")
        return
    
    plain_text = plain.lower()
    result = ''
    #verifier si a et b sont premiers avec 26, sinon raise an exception
    if math.gcd(a,26)!=1:
        raise NotCoprimeError("a has to be coprime with 26")
    else:
        for char in plain_text:
            if char.isalpha():
                scaled_char = ord(char) - ord('a')
                result += chr((scaled_char*a + b) % 26 + ord('a'))
            else:
                result += ' '
        return result
    
    
def affine_decrypt(cipher, a, b):
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        print("NUMBERS PLEASE")
        return
    
    cipher_text = cipher.lower()
    result = ''
    
    # verifier si a et b sont premiers avec 26, sinon raise an exception
    if math.gcd(a, 26) != 1:
        raise NotCoprimeError("a must be coprime with 26")
    
    # calculer l'inverse de a
    a_inverse = pow(a, -1, 26)
    
    for char in cipher_text:
        if char.isalpha():
            y = ord(char) - ord('a')
            decrypted_value = (a_inverse*((y - b)%26))%26
            result += chr(decrypted_value + ord('a'))
        else:
            result += char
    return result
    
    
try:
    encrypted = affine_encrypt("today was a great day, because i'm starting to get rid of my social anxiety slowly, but surely", 17, 20)
    print("Encrypted:", encrypted)
    
    decrypted = affine_decrypt(encrypted, 17, 20)
    print("Decrypted:", decrypted)
    
except NotCoprimeError as e:
    print(f"Error: {e}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")