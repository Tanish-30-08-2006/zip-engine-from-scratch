import os
import math
import collections

# <ADD>: This line ensures Python knows we are using standard UTF-8 encoding
# -*- coding: utf-8 -*-

def analyze_shannon_limit(content):
    total_chars = len(content)
    # <FIX>: Capital 'C' in Counter
    counts_per_char = collections.Counter(content)

    print(f"{'Char':<10} | {'ASCII':<8} | {'Ideal':<10} | {'Waste/Char':<12} | {'Total Waste (Char)'}")
    print("-" * 75)

    total_wasted_bits = 0

    for char, count in counts_per_char.items():
        p = count / total_chars
        
        # Shannon's ideal length
        # Using a tiny offset (1e-10) prevents math domain errors if p is somehow 0
        ideal_bits = -math.log2(p) if p > 0 else 0

        current_allocated_bits = 8.0 

        wasted_bits_per_character = current_allocated_bits - ideal_bits
        total_wasted_bits_per_character = wasted_bits_per_character * count
        total_wasted_bits += total_wasted_bits_per_character

        display_char = f"'{char}'" if char != " " else "Space"
        
        print(f"{display_char:<10} | {current_allocated_bits:<8.1f} | {ideal_bits:<10.4f} | {wasted_bits_per_character:<12.4f} | {total_wasted_bits_per_character:.2f} bits")

    return total_wasted_bits

def main():
    print("--- The Compression Lab: Shannon Limit & Waste Analysis ---")

    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file name (e.g., repetitive.txt): ")

   
    file_path = os.path.join(base_dir, "..", "data", file_name)

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
    
    total_bits_used_now = len(content) * 8
    final_waste_count = analyze_shannon_limit(content)

    print("-" * 75)
    print(f"RESULTS FOR: {file_name}")
    print(f"Total Bits spent using ASCII: {total_bits_used_now} bits")
    print(f"Total Bits 'Wasted':         {final_waste_count:.2f} bits")
    print(f"Efficiency Score:            {(1 - (final_waste_count / total_bits_used_now)):.2%}")
    print("-" * 75)

if __name__ == "__main__":
    main()
    