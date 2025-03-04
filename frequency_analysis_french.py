import collections
import math

def affine_decrypt(ciphertext, a, b):
    """Decrypt text using affine cipher with given key."""
    if math.gcd(a, 26) != 1:
        return ""
    
    a_inv = pow(a, -1, 26)
    result = ""
    
    for char in ciphertext.lower():
        if char.isalpha():
            # Convert to 0-25 range
            c = ord(char) - ord('a')
            # Apply decryption formula
            p = (a_inv * ((c - b) % 26)) % 26
            # Convert back to letter
            result += chr(p + ord('a'))
        else:
            result += char
    
    return result

def frequency_analysis(ciphertext):
    """Count letter frequencies in the ciphertext."""
    # Remove non-alphabetic characters and convert to lowercase
    cleaned_text = ''.join(c for c in ciphertext.lower() if c.isalpha())
    
    # Count letter occurrences
    letter_count = collections.Counter(cleaned_text)
    
    # Calculate frequencies as percentages
    total_letters = len(cleaned_text)
    frequencies = {letter: (count / total_letters) * 100 for letter, count in letter_count.items()}
    
    # Sort by frequency (highest first)
    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))

def solve_affine_parameters(p1, c1, p2, c2):
    """Solve for 'a' and 'b' given two plaintext/ciphertext mappings."""
    # First, solve for 'a': a ≡ (c1 - c2) * inv(p1 - p2) (mod 26)
    diff_p = (p1 - p2) % 26
    diff_c = (c1 - c2) % 26
    
    # Check if diff_p is invertible
    if math.gcd(diff_p, 26) != 1:
        return None
    
    # Calculate modular inverse of diff_p
    try:
        inv_diff_p = pow(diff_p, -1, 26)
    except ValueError:
        return None
    
    # Calculate 'a'
    a = (diff_c * inv_diff_p) % 26
    
    # Check if 'a' is valid (must be coprime with 26)
    if math.gcd(a, 26) != 1:
        return None
    
    # Now solve for 'b': b ≡ c1 - a*p1 (mod 26)
    b = (c1 - a * p1) % 26
    
    return (a, b)

def score_text_french(text):
    """Score a text based on common French patterns."""
    # Common French words
    common_words = ['le', 'la', 'les', 'un', 'une', 'des', 'et', 'est', 'en', 'que', 
                   'qui', 'dans', 'pour', 'pas', 'sur', 'ce', 'il', 'je', 'vous', 'de']
    
    # Common French bigrams
    common_bigrams = ['es', 'le', 'de', 'en', 'on', 'nt', 'an', 're', 'er', 'ur', 'it', 'te']
    
    score = 0
    
    # Check for common words
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
    # French letter frequencies (most common letters)
    # E, A, S, I, N, T, R, U, L, O are the most common in French
    french_freq = ['e', 'a', 's', 'i', 'n', 't', 'r', 'u', 'l', 'o']
    
    # Get frequency analysis of ciphertext
    cipher_freq = frequency_analysis(ciphertext)
    
    # Get the two most frequent letters in ciphertext
    most_common = list(cipher_freq.keys())[:2]
    if len(most_common) < 2:
        return None
    
    # Try different combinations of common letters
    possible_keys = []
    
    # Try mapping the most frequent cipher letters to common French letters
    for p1 in range(min(4, len(french_freq))):  # Try top 4 French letters for first mapping
        for p2 in range(min(4, len(french_freq))):  # Try top 4 for second mapping
            if p1 == p2:
                continue
                
            # Get the possible plaintext letters
            plain1, plain2 = ord(french_freq[p1]) - ord('a'), ord(french_freq[p2]) - ord('a')
            # Get the ciphertext letters
            cipher1, cipher2 = ord(most_common[0]) - ord('a'), ord(most_common[1]) - ord('a')
            
            # Try to solve for 'a' and 'b'
            key = solve_affine_parameters(plain1, cipher1, plain2, cipher2)
            if key:
                possible_keys.append(key)
    
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

# Example usage
if __name__ == "__main__":
    # Example French encrypted text (you can replace this with your own)
    encrypted = "lyhrywx  kh ck qyqkhf r scywfk whk cjuhoyh qushabagwk  quao rwofk qusagwk  gwkzzk lkzzk rywxhsk  yh utyxk"  # This would be an encrypted French text
    
    decrypted, key = crack_affine_cipher_french(encrypted)
    print(f"Texte chiffré: {encrypted}")
    print(f"Texte déchiffré: {decrypted}")
    print(f"Clé trouvée: a={key[0]}, b={key[1]}")
    
    # For manual inspection, you can also print letter frequencies
    print("\nAnalyse de fréquence:")
    freq = frequency_analysis(encrypted)
    for letter, percentage in freq.items():
        print(f"{letter}: {percentage:.2f}%")