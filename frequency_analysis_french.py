import collections
import math
from affine_cipher import affine_encrypt

def affine_decrypt(ciphertext, a, b):
    """Decrypt text using affine cipher with given key."""
    if math.gcd(a, 26) != 1:
        return ""
    
    a_inv = pow(a, -1, 26)
    result = ""
    
    for char in ciphertext.lower():
        if char.isalpha():
            c = ord(char) - ord('a')
            p = (a_inv * ((c - b) % 26)) % 26
            result += chr(p + ord('a'))
        else:
            result += char
    
    return result

def frequency_analysis(ciphertext):
    """Count letter frequencies in the ciphertext."""

    cleaned_text = ''.join(c for c in ciphertext.lower() if c.isalpha())
    
    letter_count = collections.Counter(cleaned_text)
    
    total_letters = len(cleaned_text)
    frequencies = {letter: (count / total_letters) * 100 for letter, count in letter_count.items()}
    
    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))

def solve_affine_parameters(p1, c1, p2, c2):
    """Solve for 'a' and 'b' given two plaintext/ciphertext mappings."""

    diff_p = (p1 - p2) % 26
    diff_c = (c1 - c2) % 26
    
    if math.gcd(diff_p, 26) != 1:
        return None
    
    try:
        inv_diff_p = pow(diff_p, -1, 26)
    except ValueError:
        return None
    
    a = (diff_c * inv_diff_p) % 26
    
    if math.gcd(a, 26) != 1:
        return None

    b = (c1 - a * p1) % 26
    
    return (a,b)



def score_text_french(text):
    """Score a text based on common French patterns."""
    # Common French words
    common_words = ['le', 'la', 'les', 'un', 'une', 'des', 'et', 'est', 'en', 'que', 
                   'qui', 'dans', 'pour', 'pas', 'sur', 'ce', 'il', 'je', 'vous', 'de',
                   'avec', 'du', 'au', 'par', 'nous', 'mais', 'ou', 'si', 'leur',
                   'sont', 'cette', 'tout', 'ces', 'plus']
    # Common French bigrams
    common_bigrams = ['es', 'le', 'de', 'en', 'on', 'nt', 'an', 're', 'er', 'ur', 'it', 'te', 'ou', 'ai']
    
    score = 0
    
    words = text.lower().split()
    for word in words:
        if word in common_words:
            score += 10
    
    # Check for common bigrams
    for i in range(len(text) - 1):
        bigram = text[i:i+2].lower()
        if bigram in common_bigrams:
            score += 1
    
    return score

def find_affine_key_french(ciphertext):
    """Try to find the affine cipher key using frequency analysis for French."""

    french_freq = ['e', 'a', 's', 'i', 'n', 't', 'r', 'u', 'l', 'o']
    

    cipher_freq = frequency_analysis(ciphertext)
    
    most_common = list(cipher_freq.keys())[:2]

    possible_keys = []

    for p1 in range(min(6, len(french_freq))): 
        for p2 in range(min(6, len(french_freq))): 
            if p1 == p2:
                continue
                
            plain1, plain2 = ord(french_freq[p1]) - ord('a'), ord(french_freq[p2]) - ord('a')

            cipher1, cipher2 = ord(most_common[0]) - ord('a'), ord(most_common[1]) - ord('a')
            
            key = solve_affine_parameters(plain1, cipher1, plain2, cipher2)
            if key:
                print(f"we will append the key {key}")
                possible_keys.append(key)
            else:
                print("no key found :( ")
    
    # Test each possible key
    best_key = None
    best_score = -1
    
    for a, b in possible_keys:
        # Decrypt using this key
        decrypted = affine_decrypt(ciphertext, a, b)
        
        # Score the decryption based on French patterns
        score = score_text_french(decrypted)
        
        if score > best_score:
            best_score = score
            best_key = (a, b)
    
    return best_key

def crack_affine_cipher_french(ciphertext):
    """Attempt to crack an affine cipher using French language patterns."""
    key = find_affine_key_french(ciphertext)
    
    if not key:
        return "Impossible de déchiffrer le texte.", (0, 0)
    
    a, b = key
    decrypted = affine_decrypt(ciphertext, a, b)
    return decrypted, key

if __name__ == "__main__":
    encrypted = "lyhrywx  rk owao khfxuah t uppxkhtxk cyqqkhf cuookx zk cjabbxkqkhf ubbahk unkc whk uhuzmok bxkgwkhfakzzk" 
    
    decrypted, key = crack_affine_cipher_french(encrypted)
    print(f"Texte chiffré: {encrypted}")
    print(f"Texte déchiffré: {decrypted}")
    print(f"Clé trouvée: a={key[0]}, b={key[1]}")
    
    print("\nAnalyse de fréquence:")
    freq = frequency_analysis(encrypted)
    for letter, percentage in freq.items():
        print(f"{letter}: {percentage:.2f}%")