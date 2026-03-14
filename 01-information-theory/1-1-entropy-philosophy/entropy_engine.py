import collections 
import os
import math

def calculate_entropy(data):
    """
    Entropy (H) is the average amount of information contained in each message.
    Formula: H = -sum(P(i) * log2(P(i))) 
    also entropy  = summation (P(i))*(information(P(i))
    """

    if not data:
        return 0
    
    total_len = len(data)
    counts_per_char = collections.Counter(data)
    entropy = 0

    print(f"\n{'Char':<10} | {'Probability':<12} | {'Contribution to Entropy'}")
    print("-" * 55)

    for char, count in counts_per_char.items():

        p = count / total_len #probability of occurance of that character inside loop

        # Calculate the 'Information' of this character
        # Logic: If a character is rare, its 'log2' value is higher (more surprise).
        # We use math.log2 because computers work in base 2 (bits).
        info_content = -math.log2(p)

        # Add to the total entropy
        # Entropy is the weighted average: Probability * Information
        entropy = entropy +  p * info_content
        
        display_char = f"'{char}'" if char != " " else "Space"
        print(f"{display_char:<10} | {p:<12.2%} | {p * info_content:.4f} bits")
    
    return entropy




def main():
    print("--- The Compression Lab: Entropy Engine ---")

    base_dir = os.path.dirname(__file__)
    
    # File path 
    file_name = input(F"Enter file name(from data folder) to fetch data from : (eg: complex.txt) :  ")
    file_path = os.path.join(base_dir,"..","data",file_name)

    # Does the file exists 
    if not os.path.exists(file_path):
        print(f"Error: The file '{filename}' was not found.")
        return
    
    with open(file_path,'r',encoding='utf-8') as file:
        file_content = file.read()
    
    total_chars = len(file_content)
    actual_entropy = calculate_entropy(file_content)

    print("-" * 55)
    print(f"Total File Size: {total_chars} bytes ({total_chars * 8} bits)")
    print(f"Calculated Entropy: {actual_entropy:.4f} bits per character")

    # If the entropy is 2 bits, but we use 8 bits (standard ASCII), 
    # we are wasting 6 bits per character!
    potential_size = (actual_entropy * total_chars) / 8
    print(f"Theoretical Compressed Size: {potential_size:.2f} bytes")
    print(f"Possible Compression: {(1 - (potential_size/total_chars)):.2%}")



if __name__ == "__main__":
    main()