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

    for sym in lit_len_stream:
        if sym == "END_OF_FILE":
            print(f"{sym:<15} | Stop Decoding                | [FINISH]")
            break
            
        if str(sym).startswith("L_"):
            # It's a Length! We must also pull a Distance.
            length = int(sym.split("_")[1])
            dist_sym = dist_stream[dist_ptr]
            distance = int(dist_sym.split("_")[1])
            dist_ptr += 1
            
            # Jump back 'distance' and copy 'length'
            back_index = len(rebuilt) - distance
            copied_chunk = ""
            for i in range(length):
                char = rebuilt[back_index + i]
                copied_chunk += char
                rebuilt += char
            
            print(f"{sym + ' ' + dist_sym:<15} | Jump -{distance}, Copy {length} ('{copied_chunk}') | {rebuilt[-15:]}")
        
        else:
            # It's just a normal character
            rebuilt += sym
            display_sym = f"'{sym}'" if sym != " " else "Space"
            print(f"{display_sym:<15} | Write Literal char          | {rebuilt[-15:]}")
            
    return rebuilt


# -------------------------------------------------------------------------
# PART 4: THE INFORMATION AUDIT (THE "PRO" LAB)
# -------------------------------------------------------------------------

def run_deflate_pro_lab():
    print("\n" + "-"*70)
    print("         DEFLATE HYBRID ENGINE: THE ULTIMATE VISUALIZER         ")
    print("-"*70)

    # 1. INPUT DATA
    base_dir = os.path.dirname(__file__)
    file_name = input("\nEnter file name from /data (e.g., repetitive.txt): ")
    file_path = os.path.join(base_dir, "..","data", file_name)

    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    # 2. ENCODING PHASE
    lit_len_stream, dist_stream = deflate_encoder_lab(original_text)

    # 3. PROBABILITY & HUFFMAN PHASE
    print("\n" + "-"*100)
    print("STEP 2: HUFFMAN PROBABILITY ANALYSIS")
    print("-"*100)
    
    # Analyze frequency of symbols in both streams
    freq_lits = collections.Counter(lit_len_stream)
    freq_dists = collections.Counter(dist_stream)
    
    # Build TWO Trees (The Pro ZIP way)
    root_lits = build_huffman_tree(freq_lits, "Literal/Length")
    root_dists = build_huffman_tree(freq_dists, "Distance")
    
    # Generate bit-codes
    codes_lits, codes_dists = {}, {}
    generate_codes(root_lits, "", codes_lits)
    generate_codes(root_dists, "", codes_dists)

    # 4. DECODING PHASE
    rebuilt_text = deflate_decoder_lab(lit_len_stream, dist_stream)

    # 5. FINAL REPORT (The "Why it worked" section)
    print("\n" + "-"*100)
    print("                     FINAL EFFICIENCY REPORT                     ")
    print("-"*100)
    
    # Calculate total bits used
    total_bits = 0
    for s in lit_len_stream: total_bits += len(codes_lits[s])
    for d in dist_stream: total_bits += len(codes_dists[d])
    
    orig_bits = len(original_text) * 8
    
    print(f"1. Original Text Length:     {len(original_text)} chars ({orig_bits} bits)")
    print(f"2. LZ77 Symbols Created:     {len(lit_len_stream)} symbols")
    print(f"3. Huffman compressed size:  {total_bits} bits")
    print(f"4. TOTAL SPACE SAVED:        {((orig_bits - total_bits) / orig_bits) * 100:.2f}%")
    print("-" * 100)
    
    if original_text == rebuilt_text:
        print("   VERIFICATION: DATA IS 100% IDENTICAL. LOSSLESS SUCCESS.")
    else:
        print("   ERROR: Data mismatch detected.")
    
    print("-"*100 + "\n")

if __name__ == "__main__":
    run_deflate_pro_lab() # Running the lab logic
