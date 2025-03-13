import math
from functools import reduce
from collections import defaultdict
from frequency_analysis import freqAnalysis
from frequency_analysis_french import score_text_french
from vigenere_cipher import vigenere_decrypt

#trouver les sequences de 3 caracteres qui se repètent
def find_repeated_sequences(ciphertext):
    cipher = ''.join(c for c in ciphertext.lower() if c.isalpha())
    
    sequences_positions = {}
    
    for i in range(len(cipher) - 2):
        seq = cipher[i:i+3]
        if seq in sequences_positions:
            sequences_positions[seq].append(i) #si la clé qui est la seq existe, append i à la liste de positions qui est la valeur
        else:
            sequences_positions[seq] = [i] # si cette clé n'existe pas on la crée et initilise la liste des indices
    
    repeated_sequences = {seq : positions for seq, positions in sequences_positions.items() if len(positions)>1} #prendre uniquement les séquences qui se repétent plus d'une fois
    return repeated_sequences # on sort avec un dict qui a les sequences comme clés et une liste des indices où ils se repétent comme valeur


def calculate_distances(repeated_sequences): #calculer les distances entre les indices
    seq_differences = {} 
    
    for seq, positions in repeated_sequences.items():
        if len(positions) < 2:
                continue
        
        for i in range(len(positions)-1):
            diff = positions[i+1] - positions[i] #on calcule les differences entre les indices deux à deux
            if seq in seq_differences:
                seq_differences[seq].append(diff)
            else:
                seq_differences[seq] = [diff]
    return seq_differences # on sort avec un dict ayant les sequences comme clés, et les differences d'indices deux à deux comme valeur
           
def find_gcd_of_list(numbers): #calcule le pgcd de plusieurs nombres
    return reduce(math.gcd, numbers)

def distances_pgcd(seq_differences):
    sequence_gcds = {}
    for seq, diffs in seq_differences.items(): #dans le dict de sequence x liste_diff 
        if diffs:
            diff_gcd = find_gcd_of_list(diffs) # on calcule le pgcd de tt les distances
            sequence_gcds[seq] = diff_gcd
    
    return sequence_gcds # on sort avec un dict ayant les sequences comme clés et le pgcd de toutes les differences comme valeur

def gcd_occurences(sequence_gcds):
    
    gcd_counter = defaultdict(int)
    
    for gcd in sequence_gcds.values(): #on calcule le nombre de fois qu'un pgcd se repéte, it will represent the most likely length of the key
        gcd_counter[gcd] += 1
    
    return dict(gcd_counter) # on sort avec un dict ayant comme clé les pgcd et comme valeur leur occurrences

def find_divisors(n): #calcule les diviseurs d'un nombre
    divisors = []
    for i in range(1, n + 1): 
        if n % i == 0:
            divisors.append(i)
    return divisors

def find_key_lengths(gcd_counter): # given un pgcd, on calcule les longueurs possibles des clés
    potential_lengths = defaultdict(int)
    
    sorted_gcds = dict(sorted(gcd_counter.items(), key=lambda x: x[1], reverse=True)) #we sort te gcds and their occurrences in descending order
    
    for gcd, count in sorted_gcds.items():
        if gcd>1:
            divisors = find_divisors(gcd) #les diviseurs du pgcd sont les valeurs possibles de la clé
            for divisor in divisors:
                if divisor>1:
                    potential_lengths[divisor] += count #on calcule le nombre d'occurrences de chaque diviseur pour voir which one is the likeliest
    
    return sorted(potential_lengths.items(), key=lambda x: x[1], reverse=True)

def split_ciphertext(ciphertext, key_length): #ceci va diviser le texte crypté en des groupes selon la longeur de la clé
    cipher = ''.join(c for c in ciphertext if c.isalpha()).lower()
    
    groups = ['']*key_length
    
    for i in range(len(cipher)):
        group_index = i % key_length
        groups[group_index] += cipher[i] #à chaque position on prend la lettre correspondante selon la longueur de la clé
    
    return groups


def determine_key(groups, ref_letter='e'):
    key = ''
    for group in groups:
        freq = freqAnalysis(group)
        if not freq:  # Skip empty groups
            continue
        # Get the most frequent letter in this group
        most_frequent = list(freq.keys())[0]
        
        # Calculate the shift needed to transform most_frequent to ref_letter
        shift = (ord(most_frequent) - ord(ref_letter)) % 26
        key_letter = chr(shift + ord('a'))
        
        key += key_letter
    
    return key

def kasiski_test(ciphertext):
    # Steps 1-4: Find key length candidates
    print("Searching for repeated sequences...")
    repeated_seqs = find_repeated_sequences(ciphertext)
    print(f"Found {len(repeated_seqs)} repeated sequences.")
    
    print("Calculating distances...")
    distances = calculate_distances(repeated_seqs)
    
    print("Finding GCDs...")
    gcds = distances_pgcd(distances)
    
    print("Counting GCD occurrences...")
    gcd_counts = gcd_occurences(gcds)
    
    print("Determining potential key lengths...")
    potential_key_lengths = find_key_lengths(gcd_counts)
    print(f"Top key length candidates: {potential_key_lengths[:5]}")
    
    results = []
    
    # Try each promising key length
    for key_length, score in potential_key_lengths[:5]:  # Try top 5 candidates
        print(f"\nTrying key length: {key_length}")
        # Split ciphertext into groups
        groups = split_ciphertext(ciphertext, key_length)
        
        # Try multiple reference letters for frequency analysis
        best_key = ""
        best_score = -1
        best_plaintext = ""
        
        reference_letters = ['e', 'a', 's', 'i', 'n']  # Most common French letters
        
        for ref_letter in reference_letters:
            # Determine key using this reference letter
            key = determine_key(groups, ref_letter)
            # Decrypt using this key
            plaintext = vigenere_decrypt(ciphertext, key)
            # Score the plaintext
            text_score = score_text_french(plaintext)
            
            if text_score > best_score:
                best_score = text_score
                best_key = key
                best_plaintext = plaintext
        
        results.append((key_length, best_key, best_plaintext, best_score))
        
        # Print results
        print(f"Key length: {key_length}, Key: {best_key}, Score: {best_score}")
        print(f"Decryption sample: {best_plaintext[:100]}...")  # Show first 100 chars
    
    # Sort results by score
    results.sort(key=lambda x: x[3], reverse=True)
    return results


if __name__ == "__main__":
    results = kasiski_test("MAXSMWJOERYVDLVGYVUUESFHNEEHYVTEEHCHMPFILJBRRBNLSLRGYFVRZHYGFSGFIFFSJIMFSYGHIJSAGVCTVEJIHHHEJHCROEWTCFBCVRYVDLVGJHSMVHXHHEESLHSDZGNUJBLSLHUSKCWNFRCSMFMEJRYPBNZSLHTETILLTEVZOWJLZGUWJOERYPPDLZYVEEJSWXSIKSGDUEIWYOTRVBZRSCVQYWUEXSMWJOESHSSOKSAHBNKZYVDLVGWROTISFHTATQYVOOEOOWPRZGYVVNVPIQOEXSMWJOERYVDLVGYVUCIIWLBLVDIXSMRWHWFNZFFDTETILLUEUSMVZSKSGHTCIMJWPGIOJKJQLSMFBRLBYFMETCGSSODWMHQELHYQURRWHHSDVGPLPLRHCROSUSXRONVSMVJGEWZLDAKWPHT")
    
    print("\n===== FINAL RESULTS =====")
    for key, plaintext in results:
        print(f"Key: {key}")
        print(f"Decryption sample: {plaintext[:200]}")
        print("-" * 50)