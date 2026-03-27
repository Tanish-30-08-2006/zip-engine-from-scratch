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
