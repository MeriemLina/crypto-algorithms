import collections
import math
from affine_cipher import affine_decrypt


def crack_affine_cipher(ciphertext):
    key = find_affine_key(ciphertext)
    if not key:
        return "could not crack the cipher"
    
    a,b = key
    decrypted = affine_decrypt(ciphertext, a, b)
    return decrypted, key


def find_affine_key(ciphertext):
    english_freq = ['e','t','a','o','i','n','s','h']
    cipher_freq = freqAnalysis(ciphertext)
    
    most_common = list(cipher_freq.keys())[:2] #review this
    
    possible_keys = []
    
    for p1 in range(min(4,len(english_freq))):
        for p2 in range(min(4, len(english_freq))):
            if p1 == p2: continue
            
            plain1, plain2= ord(english_freq[p1] )- ord('a'), ord(english_freq[p2] )- ord('a')
            cipher1, cipher2 = ord(most_common[0]) - ord('a'), ord(most_common[1]) - ord('a')
            
            key = solve_affine_parameters(cipher1, cipher2, plain1, plain2)
            
            if key:
                possible_keys.append(key)
    #apres avoir eu toutes nos clés possibles, on cherche quelle est la plus correcte
    
    best_key = None
    best_score = -1
    for a,b in possible_keys:
        decrypted = affine_decrypt(ciphertext,a,b)
        
        score = score_text(decrypted)
        if score > best_score:
            best_score = score
            best_key = (a,b)
    
    return best_key
    

def freqAnalysis(ciphertext):
    #nettoyer la chaine
    cleaned_text = ''.join(c for c in ciphertext.lower() if c.isalpha())
    
    #utiliser collections pour compter le nombre d'occurences
    letter_counter = collections.Counter(cleaned_text)
    
    #calculate the frequencies
    total_letters = len(cleaned_text)
    frequencies = {letter : (count / total_letters)*100 for letter, count in letter_counter.items()}
    
    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True)) #review



def solve_affine_parameters(c1, c2, p1, p2):
    diff_c = (c1 - c2) % 26
    diff_p = (p1 - p2) % 26
    
    if math.gcd(diff_p,26) != 1:
        return None
    
    try:
        inv_diff_p = pow(diff_p, -1, 26)
    except ValueError:
        return None
    
    a = (diff_c * inv_diff_p)%26
    
    if math.gcd(a, 26) != 1:
        return None
    
    
    b = (c1 - a*p1)%26
    return (a,b)

def score_text(text):
    common_words = ['the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but']
    common_bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd']
    
    
    words = text.lower().split()
    score = 0
    
    for word in words:
        if word in common_words:
            score += 10
    
    for i in range(len(text) - 1):
        bigram = text[i:i+2].lower()
        if bigram in common_bigrams:
            score += 1
    
    return score

if __name__ == "__main__":
    # Example encrypted text
    encrypted = "fytum euo u sxkuf tum lkcuwok a q ofuxfahs fy skf xat yb qm oycauz uhvakfm ozyezm lwf owxkzm zkf o jypk byx fjk lkof"
    
    decrypted, key = crack_affine_cipher(encrypted)
    print(f"Ciphertext: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Key found: a={key[0]}, b={key[1]}")
    
    # For manual inspection, you can also print letter frequencies
    print("\nFrequency Analysis:")
    freq = freqAnalysis(encrypted)
    for letter, percentage in freq.items():
        print(f"{letter}: {percentage:.2f}%")