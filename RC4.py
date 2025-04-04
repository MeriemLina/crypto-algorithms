def KSA(key):
    key_length = len(key) #save la longeur de la clé
    S = list(range(256)) #initialize a list of 256 values
    j = 0
    
    for i in range(256):
        j = (j + S[i] + key[i % key_length])%256 #calculer la nouvelle valeur de j
        S[i], S[j] = S[j], S[i] #swap the two values
    
    return S

def PRGA(S,data_length):
    i = 0
    j = 0
    keystream = []
    
    for _ in range(data_length):
        i = (i +1)%256
        j = (j + S[i])%256
        S[i], S[j] = S[j], S[i]
        sum = (S[i]+ S[j])%256
        keystream.append(S[sum] )
    
    return keystream

def RC4(key, data):
    if isinstance(key, str):
        key = bytearray(key.encode()) #the bytearray will take each character of the string and save their ascii in a list
    if isinstance(data,str):
        data = bytearray(data.encode())
    
    S = KSA(key)
    keystream = PRGA(S,len(data))
    result = bytearray()
    
    for i in range(len(data)):
        result.append(data[i]^keystream[i])
    
    return result

if __name__ == "__main__":
    key = "Key"
    plaintext = "Hello, World!"
    
    # Encrypt
    ciphertext = RC4(key, plaintext)
    print("Encrypted:", ' '.join(format(x, '02x') for x in ciphertext))
    
    # Decrypt 
    decrypted = RC4(key, ciphertext)
    print("Decrypted:", decrypted.decode())