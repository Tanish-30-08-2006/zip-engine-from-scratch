# -*- coding: utf-8 -*-
import os
import heapq
import collections

# =========================================================================
# PHASE 1 & 2: THE HUFFMAN ARCHITECTURE
# =========================================================================

class HuffmanNode:
    """ Represents a single leaf or branch in our bit-tree """
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    """ Connects symbols into a tree based on their probability """
    heap = [HuffmanNode(sym, f) for sym, f in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo, hi = heapq.heappop(heap), heapq.heappop(heap)
        merged = HuffmanNode(None, lo.freq + hi.freq)
        merged.left, merged.right = lo, hi
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, current_code, mapping):
    """ Traverses the tree to find the 0s and 1s for each symbol """
    if not node: return
    if node.symbol is not None:
        mapping[node.symbol] = current_code
        return
    generate_codes(node.left, current_code + "0", mapping)
    generate_codes(node.right, current_code + "1", mapping)


# =========================================================================
# PHASE 3: THE LZ77 ENGINE (PATTERN FINDER)
# =========================================================================

def lz77_process(text, window_size=400):
    """ Scans text for repeats and returns a list of symbols """
    symbols = []
    cursor = 0
    print(f"\n[LZ77] Scanning {len(text)} characters for patterns...")
    
    while cursor < len(text):
        best_dist, best_len = 0, 0
        search_start = max(0, cursor - window_size)
        
        # Searching the past
        for start_pos in range(search_start, cursor):
            curr_len = 0
            while (cursor + curr_len < len(text) and 
                   text[start_pos + curr_len] == text[cursor + curr_len]):
                curr_len += 1
            if curr_len > best_len:
                best_len, best_dist = curr_len, cursor - start_pos

        # Only use a match if it's 3+ characters (The 'Worth It' Rule)
        if best_len >= 3:
            symbols.append(f"L{best_len}_D{best_dist}")
            cursor += best_len
        else:
            symbols.append(text[cursor]) # Keep it as a Literal character
            cursor += 1
    
    symbols.append("EOF_MARKER") # Add end of file signal
    return symbols


# =========================================================================
# PHASE 4: THE PHYSICAL ARCHIVE (BIT-PACKING & HEADERS)
# =========================================================================

class BitPacker:
    """ The 'Funnel' that packs 0/1 strings into 8-bit Bytes """
    def __init__(self):
        self.output = bytearray()
        self.current_byte = 0
        self.bits_filled = 0

    def push_bits(self, bit_string):
        """ Pour Huffman bits into the bucket """
        for bit in bit_string:
            self.current_byte = (self.current_byte << 1) | int(bit)
            self.bits_filled += 1
            if self.bits_filled == 8:
                self.output.append(self.current_byte)
                self.current_byte = 0
                self.bits_filled = 0

    def flush(self):
        """ Pads the final byte with zeros if it's not full """
        if self.bits_filled > 0:
            self.current_byte <<= (8 - self.bits_filled)
            self.output.append(self.current_byte)
        return self.output


# =========================================================================
# THE GRAND GENERALIZED EXECUTION
# =========================================================================

def main_compression_factory():
    print("\n" + "--"*80)
    print("         THE ULTIMATE GENERALIZED COMPRESSION LABORATORY         ")
    print("--"*80)

    # 1. FILE INGESTION
    file_name = input("\nEnter file to compress from /data folder (e.g., repetitive.txt): ")
    # Building the path dynamically (Assuming /data is at the project root)
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "data", file_name)

    if not os.path.exists(file_path):
        print(f" ERROR: File '{file_path}' not found!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    start_size = len(original_text)
    print(f"\n[1] INPUT LOADED: '{file_name}' ({start_size} characters)")

    # 2. RUN LZ77 (Pattern Substitution)
    symbol_stream = lz77_process(original_text)
    print(f"    - Pattern Finding Complete. Resulted in {len(symbol_stream)} Symbols.")

    # 3. BUILD HUFFMAN MAP (The Bit-Instructions)
    print("\n[2] BUILDING HUFFMAN DICTIONARY...")
    freqs = collections.Counter(symbol_stream)
    root = build_huffman_tree(freqs)
    huffman_codes = {}
    generate_codes(root, "", huffman_codes)
    
    # Store Bit-Lengths for the Header (Canonical Style)
    bit_lengths = {sym: len(code) for sym, code in huffman_codes.items()}
    print(f"    - Dictionary Built. Unique Symbols: {len(huffman_codes)}")

    # 4. PHYSICAL ASSEMBLY (Writing to Binary)
    print("\n[3] ASSEMBLING PHYSICAL ARCHIVE (HEX & BIT PACKING)...")
    packer = BitPacker()
    final_archive = bytearray()

    # --- THE HEADER ---
    # Signature 'PK'
    print("    - Writing Magic Signature: 0x50 0x4B (P K)")
    final_archive.append(ord('P'))
    final_archive.append(ord('K'))

    # Filename
    print(f"    - Embedding Filename: '{file_name}'")
    final_archive.append(len(file_name))
    for char in file_name:
        final_archive.append(ord(char))

    # The Map (Crucial for Generalization)
    print(f"    - Packing Huffman Map ({len(bit_lengths)} entries)...")
    final_archive.append(len(bit_lengths)) # Number of symbols
    for sym, length in bit_lengths.items():
        # This is a simple way to store the map for this lab
        # Real ZIPs use more complex binary headers
        sym_str = str(sym)
        final_archive.append(len(sym_str)) # How long is the symbol name?
        for c in sym_str: final_archive.append(ord(c))
        final_archive.append(length) # How many bits is its code?

    # --- THE PAYLOAD ---
    print("    - Converting Symbols to Bitstream...")
    full_bitstream = "".join([huffman_codes[s] for s in symbol_stream])
    
    print(f"    - Packing {len(full_bitstream)} bits into 8-bit Bytes...")
    compressed_bytes = packer.push_bits(full_bitstream)
    packed_data = packer.flush()
    final_archive.extend(packed_data)

    # 5. FINAL REPORT
    print("\n" + "--"*80)
    print("                     COMPRESSION SUMMARY REPORT                     ")
    print("--"*80)
    print(f"Original Size:   {start_size} Bytes")
    print(f"Archive Size:    {len(final_archive)} Bytes")
    print(f"Space Saved:     {((start_size - len(final_archive)) / start_size) * 100:.2f}%")
    print(f"HEX Preview:     {final_archive[:16].hex(' ').upper()} ...")
    
    output_path = file_name.split('.')[0] + ".bin"
    with open(output_path, "wb") as f:
        f.write(final_archive)
    
    print(f"\n SUCCESS: '{output_path}' created in the current directory.")
    print("This file contains the Signature, the Filename, the Map, and the Bits.")
    print("--"*80 + "\n")

if __name__ == "__main__":
    main_compression_factory()

