# -*- coding: utf-8 -*-
import os

# -------------------------------------------------------------------------
# PART 1: THE ENCODER (THE PATTERN FINDER)
# -------------------------------------------------------------------------

def lz77_encode(text, window_size=20):
    """
    Scans the text and replaces repeats with (Distance, Length, NextChar)
    """
    compressed_pointers = []
    cursor = 0

    while cursor < len(text):
        best_match_distance = 0
        best_match_length = 0
        
        # Define where our "Memory" (Search Buffer) starts
        search_start = max(0, cursor - window_size)
        
        # Compare current position against every possible start point in the past
        for start_pos in range(search_start, cursor):
            current_match_length = 0
            
            # Character-by-character comparison (Supports Overlap!)
            while (cursor + current_match_length < len(text) and 
                   text[start_pos + current_match_length] == text[cursor + current_match_length]):
                current_match_length += 1
            
            # Keep the longest match found so far
            if current_match_length >= best_match_length:
                best_match_distance = cursor - start_pos
                best_match_length = current_match_length
        
        # Move cursor past the match
        cursor += best_match_length
        
        # Grab the character that broke the match
        if cursor < len(text):
            next_char = text[cursor]
        else:
            next_char = ""
            
        compressed_pointers.append((best_match_distance, best_match_length, next_char))
        
        # Advance cursor past the next_char
        cursor += 1

    return compressed_pointers


# -------------------------------------------------------------------------
# PART 2: THE DECODER (THE RECONSTRUCTOR)
# -------------------------------------------------------------------------

def lz77_decode(pointers):
    """
    Uses the pointers to rebuild the original text bit by bit.
    """
    rebuilt_text = ""

    for distance, length, next_char in pointers:
        # If there is a pattern to copy
        if distance > 0:
            # Jump back 'distance' from where we are right now
            start_index = len(rebuilt_text) - distance
            
            # Copy 'length' characters one by one (to handle overlap)
            for i in range(length):
                char_to_copy = rebuilt_text[start_index + i]
                rebuilt_text += char_to_copy
        
        # Always add the NextChar that followed the match
        if next_char:
            rebuilt_text += next_char
            
    return rebuilt_text


# -------------------------------------------------------------------------
# PART 3: THE LABORATORY EXECUTION
# -------------------------------------------------------------------------

def run_lz77_round_trip():
    print("\n" + "="*60)
    print("      PHASE 3.1: LZ77 ROUND-TRIP VERIFICATION LAB      ")
    print("="*60)

    # 1. SETUP & PATHING
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file to test (e.g., repetitive.txt): ")
    # Correcting path to go up to /data
    file_path = os.path.join(base_dir, "..",  "data", file_name)

    if not os.path.exists(file_path):
        print(f"Error: Could not find '{file_path}'")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # 2. ENCODING (Compression)
    print(f"\n[Step 1] Encoding '{file_name}'...")
    # Using a 30-character window for better pattern matching
    pointers = lz77_encode(original_content, window_size=30)
    print(f"  > Generated {len(pointers)} LZ77 Pointers.")

    # 3. DECODING (Decompression)
    print("\n[Step 2] Decoding Pointers back to Text...")
    decoded_content = lz77_decode(pointers)

    # 4. VERIFICATION & STATS
    print("\n[Step 3] Final Verification Audit:")
    print("-" * 45)
    
    if original_content == decoded_content:
        print("RESULT: SUCCESS! (Data is 100% Identical)")
    else:
        print("RESULT: FAILED! (Data Corruption Detected)")
        # Show where it failed if small enough
        print(f"Original: {original_content[:30]}...")
        print(f"Decoded:  {decoded_content[:30]}...")

    # Logic Check: Efficiency
    original_size = len(original_content)
    # A rough estimate of "size" since we haven't bit-packed yet
    print(f"Original Characters: {original_size}")
    print(f"Number of Pointers:  {len(pointers)}")
    print("-" * 45)
    print("="*60 + "\n")

if __name__ == "__main__":
    run_lz77_round_trip()