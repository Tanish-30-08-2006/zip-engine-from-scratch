

# LZ77 DATA COMPRESSION TECHNIQUE IS SAME AS LZ1 DATA COMPRESSION TECHNIQUE 
# LZ77 / LZ1 / SLIDING WINDOW  --> DYNAMIC (ADAPTIVE) DICTIONARY TECHNIQUE

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
        search_buffer = text[search_start : cursor]
        
        # 2. DEFINE THE LOOK-AHEAD (THE FUTURE)
        # What are we trying to find a match for?
        look_ahead = text[cursor:]

        # 3. SEARCH FOR THE LONGEST MATCH
        # We try to find the longest part of 'look_ahead' inside 'search_buffer'
        for length in range(1, len(look_ahead)):
            substring = look_ahead[:length]
            
            # Find the last (most recent) occurrence of this substring in the past
            # rfind returns the index of the match
            match_index = search_buffer.rfind(substring)
            
            if match_index != -1:
                # We found a match! Calculate how far back it is.
                # Distance = (Length of search buffer) - (Index where match started)
                best_match_distance = len(search_buffer) - match_index
                best_match_length = length
            else:
                # No longer match found, stop searching for this cursor position
                break

        # 4. CREATE THE TUPLE (Pointer)
        # Move the cursor forward by (length of match + 1 for the new char)
        cursor += best_match_length
        
        # If we reached the absolute end, there is no 'next_char'
        if cursor < len(text):
            next_char = text[cursor]
        else:
            next_char = ""
            
        # Store the (Distance, Length, Character)
        compressed_data.append((best_match_distance, best_match_length, next_char))
        
        # Move cursor to the next starting point
        cursor += 1

    return compressed_data

def run_lz77_lab():
    print("\n" + "="*50)
    print("      PHASE 3.1: THE LZ77 PATTERN FINDER      ")
    print("="*50)

    # Path Setup 
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file name (e.g., repetitive.txt): ")

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

