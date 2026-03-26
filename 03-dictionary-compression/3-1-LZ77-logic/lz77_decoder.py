# -*- coding: utf-8 -*-
import os

def lz77_decode(compressed_pointers):
    """
    The LZ77 Decoder: Reconstructs the original text from (Dist, Len, Char) tuples.
    """
    # This will hold our final reconstructed text
    reconstructed_text = ""

    print("\n[Step 1] Starting Reconstruction...")

    for i, (distance, length, next_char) in enumerate(compressed_pointers):
        
        # LOGIC: If distance is 0, there is no pattern to copy.
        # We only add the next_char.
        if distance > 0:
            # Calculate the starting point in our CURRENT string
            start_index = len(reconstructed_text) - distance
            
            # We copy 'length' amount of characters
            for j in range(length):
                # We pull the character from the past and add it to the future
                # Note: Doing it char-by-char handles the 'overlap' case automatically!
                char_to_copy = reconstructed_text[start_index + j]
                reconstructed_text += char_to_copy
        
        # After copying the pattern (if any), we add the 'Next Character'
        if next_char:
            reconstructed_text += next_char
            
        # Optional: Print progress for the first few pointers
        if i < 5:
            print(f"  > Pointer {i}: Rebuilt up to -> '{reconstructed_text}'")

    return reconstructed_text

def run_lz77_decoder_lab():
    print("\n" + "="*50)
    print("      PHASE 3.1: THE LZ77 RECONSTRUCTOR (DECODER)      ")
    print("="*50)

    # For this lab, let's simulate the input from the Encoder
    # In Phase 4, we will read this from a real file.
    print("\n[Simulation] Let's decode: (0,0,'A'), (0,0,'B'), (2,2,'!')")
    
    test_pointers = [
        (0, 0, 'A'), 
        (0, 0, 'B'), 
        (2, 2, '!')  # Jump back 2 (to A), copy 2 (AB), add !
    ]

    # --- EXECUTION ---
    result = lz77_decode(test_pointers)

    print("-" * 45)
    print(f"FINAL DECODED TEXT: {result}")
    print("-" * 45)

    # --- VERIFICATION TEST ---
    # Let's try a more complex one: 'BANANA' logic
    # B, A, N, (2, 2, '!') -> BAN + AN + ! = BANAN!
    banana_pointers = [(0,0,'B'), (0,0,'A'), (0,0,'N'), (2,2,'!')]
    print(f"\nTesting 'BANANA' Logic: {lz77_decode(banana_pointers)}")
    
    print("\nLOGIC: The Decoder 'walks' the pointers to rebuild the map.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_lz77_decoder_lab()