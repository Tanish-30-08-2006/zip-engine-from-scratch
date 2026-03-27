# -*- coding: utf-8 -*-
import os
import heapq
import collections
import time

# -------------------------------------------------------------------------
# PART 1: THE HUFFMAN ARCHITECTURE (The "Bit-Squeezer")
# -------------------------------------------------------------------------

class HuffmanNode:
    """ A simple node that represents a Symbol (Char or Length/Dist) """
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        # This tells the Priority Queue to sort by frequency
        return self.freq < other.freq

def build_huffman_tree(frequencies, tree_name):
    """ Standard Huffman Tree Builder with extra console info """
    print(f"  [Huffman] Building '{tree_name}' Tree for {len(frequencies)} unique symbols...")
    heap = [HuffmanNode(sym, f) for sym, f in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        merged = HuffmanNode(None, lo.freq + hi.freq)
        merged.left, merged.right = lo, hi
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, current_code, mapping):
    """ Recursively finds the 0s and 1s for each symbol """
    if not node:
        return
    if node.symbol is not None:
        mapping[node.symbol] = current_code
        return
    generate_codes(node.left, current_code + "0", mapping)
    generate_codes(node.right, current_code + "1", mapping)


# -------------------------------------------------------------------------
# PART 2: THE DUAL-STREAM ENCODER (The "Pattern Finder")
# -------------------------------------------------------------------------

def deflate_encoder_lab(text, window_size=50):
    """
    Step 1 of DEFLATE: Break text into Literals and Distance/Length pairs.
    """
    lit_len_stream = []  # Stores Chars and Match-Lengths
    dist_stream = []     # Stores Match-Distances
    cursor = 0
    
    print("\n" + "-"*30)
    print("STEP 1: LZ77 PATTERN SCANNING")
    print("-"*30)
    print(f"{'Position':<10} | {'Action':<25} | {'Symbol Generated'}")

    while cursor < len(text):
        best_dist, best_len = 0, 0
        search_start = max(0, cursor - window_size)
        
        # Look back into the 'Past' (Search Buffer)
        for start_pos in range(search_start, cursor):
            curr_len = 0
            # How many characters in a row match the 'Future'?
            while (cursor + curr_len < len(text) and 
                   text[start_pos + curr_len] == text[cursor + curr_len]):
                curr_len += 1
            
            # If we find a longer repeat, save it
            if curr_len > best_len:
                best_len = curr_len
                best_dist = cursor - start_pos

        # DEFLATE DECISION: Is the match worth a pointer? (Min 3 chars)
        if best_len >= 3:
            match_text = text[cursor:cursor+best_len]
            print(f"{cursor:<10} | Found '{match_text}' (D:{best_dist}) | LEN_{best_len} & DIST_{best_dist}")
            
            lit_len_stream.append(f"L_{best_len}")
            dist_stream.append(f"D_{best_dist}")
            cursor += best_len
        else:
            # No repeat found? Just save the single character
            char = text[cursor]
            display_char = f"'{char}'" if char != " " else "Space"
            print(f"{cursor:<10} | No match found          | Literal {display_char}")
            
            lit_len_stream.append(char)
            cursor += 1
            
    lit_len_stream.append("END_OF_FILE")
    return lit_len_stream, dist_stream


# -------------------------------------------------------------------------
# PART 3: THE DECODER (The "Reconstructor")
# -------------------------------------------------------------------------

def deflate_decoder_lab(lit_len_stream, dist_stream):
    """
    Step 2 of DEFLATE: Turn symbols back into original text.
    """
    rebuilt = ""
    dist_ptr = 0 # Keeps track of which distance to use next
    
    print("\n" + "-"*30)
    print("STEP 3: DEFLATE DECODING (RECONSTRUCTION)")
    print("-"*30)
    print(f"{'Symbol':<15} | {'Logic Applied':<30} | {'Current Output'}")

