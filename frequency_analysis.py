import collections
import math
from typing import Dict, Tuple, List, Optional

def frequency_analysis(ciphertext: str) -> Dict[str, float]:
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

def find_affine_key(ciphertext: str) -> Optional[Tuple[int, int]]:
    """Try to find the affine cipher key using frequency analysis."""
    # English letter frequencies (most common letters)
    english_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']
    
    # Get frequency analysis of ciphertext
    cipher_freq = frequency_analysis(ciphertext)
    
    # Get the two most frequent letters in ciphertext
    most_common = list(cipher_freq.keys())[:2]
    if len(most_common) < 2:
        return None
    
    # Try different combinations of common letters
    possible_keys = []
    
    # We'll try mapping the most frequent cipher letters to common English letters
    for p1 in range(min(4, len(english_freq))):  # Try top 4 English letters for first mapping
        for p2 in range(min(4, len(english_freq))):  # Try top 4 for second mapping
            if p1 == p2:
                continue
                
            # Get the possible plaintext letters
            plain1, plain2 = ord(english_freq[p1]) - ord('a'), ord(english_freq[p2]) - ord('a')
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
        
        # Score the decryption (simple approach: count common English words)
        score = score_text(decrypted)
        
        if score > best_score:
            best_score = score
            best_key = (a, b)
    
    return best_key

def solve_affine_parameters(p1: int, c1: int, p2: int, c2: int) -> Optional[Tuple[int, int]]:
    """Solve for 'a' and 'b' given two plaintext/ciphertext mappings."""
    # We need to solve the system:
    # c1 ≡ a*p1 + b (mod 26)
    # c2 ≡ a*p2 + b (mod 26)
    
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

def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
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

def score_text(text: str) -> float:
    """Score a text based on common English patterns."""
    # This is a simplified scoring - in a real implementation you would
    # use n-gram frequencies or a dictionary of English words
    common_words = ['the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but']
    common_bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd']
    
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

def crack_affine_cipher(ciphertext: str) -> Tuple[str, Tuple[int, int]]:
    """Attempt to crack an affine cipher using frequency analysis."""
    key = find_affine_key(ciphertext)
    
    if not key:
        return "Could not crack cipher.", (0, 0)
    
    a, b = key
    decrypted = affine_decrypt(ciphertext, a, b)
    return decrypted, key

# Example usage
if __name__ == "__main__":
    # Example encrypted text
    encrypted = "fytum euo u sxkuf tum  lkcuwok a q ofuxfahs fy skf xat yb qm oycauz uhvakfm ozyezm  lwf owxkzm  zkf o jypk byx fjk lkof"  # This is "lina is amazing" encrypted with a=17, b=20
    
    decrypted, key = crack_affine_cipher(encrypted)
    print(f"Ciphertext: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Key found: a={key[0]}, b={key[1]}")
    
    # For manual inspection, you can also print letter frequencies
    print("\nFrequency Analysis:")
    freq = frequency_analysis(encrypted)
    for letter, percentage in freq.items():
        print(f"{letter}: {percentage:.2f}%")