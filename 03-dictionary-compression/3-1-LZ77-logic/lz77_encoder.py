# LZ77 DATA COMPRESSION TECHNIQUE IS SAME AS LZ1 DATA COMPRESSION TECHNIQUE 
# LZ77 / LZ1 / SLIDING WINDOW --> DYNAMIC (ADAPTIVE) DICTIONARY TECHNIQUE

'''
look ahead buffer size + search buffer size = window size 
search buffer -->(past) a fixed size window of characters algorithm has already processed
look ahead buffer --> (future) a fixed size window of characters waiting to be encoded
'''

import os

def lz77_encode(text, window_size=20):
    """
    The LZ77 Encoder: Replaces repeating patterns with (Distance, Length, Char)
    """
    compressed_data = []
    cursor = 0  # Our current position in the text

    while cursor < len(text):
        best_match_distance = 0
        best_match_length = 0
        
        # 1. DEFINE THE SEARCH BUFFER (THE PAST)
        # We look back 'window_size' steps, but not before the start of the file
        search_start = max(0, cursor - window_size)
        
        # 2. DEFINE THE LOOK-AHEAD (THE FUTURE)
        # (The look-ahead starts at text[cursor:])

        # 3. SEARCH FOR THE LONGEST MATCH (Including overlap)
        # We try to find the longest part of the look-ahead inside the search buffer area
        for start_pos in range(search_start, cursor):
            current_match_length = 0
            
            # Compare char by char from this start_pos
            # This allows the match to extend past 'cursor' (overlap)
            while (cursor + current_match_length < len(text) and 
                   text[start_pos + current_match_length] == text[cursor + current_match_length]):
                current_match_length += 1
            
            # If this is the longest match we've seen so far, save it
            if current_match_length >= best_match_length:
                best_match_distance = cursor - start_pos
                best_match_length = current_match_length
        
        # 4. CREATE THE TUPLE (Pointer)
        # Move the cursor forward by the length of the match
        cursor += best_match_length
        
        # If we reached the absolute end, there is no 'next_char'
        if cursor < len(text):
            next_char = text[cursor]
        else:
            next_char = ""
            
        # Store the (Distance, Length, Character)
        compressed_data.append((best_match_distance, best_match_length, next_char))
        
        # Move cursor to the next character (the one after the pointer)
        cursor += 1

    return compressed_data

def run_lz77_lab():
    print("\n" + "="*50)
    print("      PHASE 3.1: THE LZ77 PATTERN FINDER      ")
    print("="*50)

    # Path Setup 
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file name (e.g., lz77_test.txt): ")

    file_path = os.path.join(base_dir, "..", "data", file_name)

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- EXECUTION ---
    print(f"\n[Step 1] Analyzing patterns in '{file_name}'...")
    # Using a small window of 15 for easy viewing
    encoded_pointers = lz77_encode(content, window_size=15)

    print("\n[Step 2] Resulting LZ77 Pointers:")
    print("-" * 45)
    print(f"{'Index':<6} | {'(Dist, Len, Char)':<20}")
    print("-" * 45)

    for i, pointer in enumerate(encoded_pointers):
        print(f"{i:<6} | {str(pointer):<20}")

    # --- INSIGHTS ---
    print("-" * 45)
    total_pointers = len(encoded_pointers)
    original_chars = len(content)
    
    print(f"\nOriginal Characters: {original_chars}")
    print(f"Total LZ77 Pointers: {total_pointers}")
    print("\nLOGIC: If 'Pointers' < 'Characters', we have compressed data!")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_lz77_lab()
