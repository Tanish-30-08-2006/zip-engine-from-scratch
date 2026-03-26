# -*- coding: utf-8 -*-
import os
import time

# -------------------------------------------------------------------------
# PART 1: THE VISUAL ENCODER
# -------------------------------------------------------------------------

def lz77_encode_visual(text, window_size=20):
    compressed_pointers = []
    cursor = 0

    print("\n[ENCODING VISUALIZATION]")
    print(f"{'Buffer (Past)':<22} | {'Future':<15} | {'Pointer Found'}")
    print("-" * 60)

    while cursor < len(text):
        best_match_distance = 0
        best_match_length = 0
        
        # Define Search Buffer
        search_start = max(0, cursor - window_size)
        search_buffer = text[search_start:cursor]
        look_ahead = text[cursor:cursor + 10] # Show next 10 chars

        # Search Logic
        for start_pos in range(search_start, cursor):
            current_match_length = 0
            while (cursor + current_match_length < len(text) and 
                   text[start_pos + current_match_length] == text[cursor + current_match_length]):
                current_match_length += 1
            
            if current_match_length >= best_match_length:
                best_match_distance = cursor - start_pos
                best_match_length = current_match_length
        
        # Prepare for output
        match_len_to_skip = best_match_length
        cursor += match_len_to_skip
        next_char = text[cursor] if cursor < len(text) else ""
        
        pointer = (best_match_distance, best_match_length, next_char)
        compressed_pointers.append(pointer)

        # DISPLAY THE STEP
        past_display = search_buffer[-20:] # Show last 20 chars of past
        future_display = look_ahead[:5]    # Show next 5 chars of future
        print(f"{past_display:>22} | {future_display:<15} | {str(pointer)}")

        cursor += 1 # Advance past the next_char
    
    return compressed_pointers


# -------------------------------------------------------------------------
# PART 2: THE VISUAL DECODER
# -------------------------------------------------------------------------

def lz77_decode_visual(pointers):
    rebuilt_text = ""
    print("\n[DECODING VISUALIZATION]")
    print(f"{'Pointer':<15} | {'Action':<25} | {'Resulting String'}")
    print("-" * 70)

    for dist, length, char in pointers:
        action = ""
        if dist > 0:
            action = f"Back {dist}, Copy {length}"
            start_index = len(rebuilt_text) - dist
            for i in range(length):
                rebuilt_text += rebuilt_text[start_index + i]
        else:
            action = "No Match"
        
        if char:
            rebuilt_text += char
            action += f" + '{char}'"

        # Display the growth of the string
        display_str = rebuilt_text[-30:] # Show last 30 chars
        print(f"{str((dist, length, char)):<15} | {action:<25} | ...{display_str}")

    return rebuilt_text


# -------------------------------------------------------------------------
# PART 3: RUN LAB
# -------------------------------------------------------------------------

def run_visual_lab():
    # TEST DATA: Using a repetitive string to show the power of LZ77
    test_content = "ABCABCABCABC" 
    
    # Optional: Load from file if you prefer
    choice = input("Use default test string 'ABCABCABCABC'? (y/n): ")
    if choice.lower() == 'n':
        base_dir = os.path.dirname(__file__)
        file_name = input("Enter file name (e.g., repetitive.txt): ")
        file_path = os.path.join(base_dir, "..", "data", file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f: test_content = f.read()

    # Run the Visual Round-Trip
    pointers = lz77_encode_visual(test_content, window_size=20)
    final_text = lz77_decode_visual(pointers)

    print("\n" + "="*50)
    if test_content == final_text:
        print("VERIFICATION: SUCCESS! Data matches perfectly.")
    else:
        print("VERIFICATION: FAILED.")
    print("="*50)

if __name__ == "__main__":
    run_visual_lab()