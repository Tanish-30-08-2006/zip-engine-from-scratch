# -*- coding: utf-8 -*-
import heapq
import os
import collections

# --- HUFFMAN COMPONENTS ---
class HuffmanNode:
    def __init__(self, char, freq):
        self.char, self.freq = char, freq
        self.left = self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(text):
    
    counts = collections.Counter(text)
    heap = [HuffmanNode(c, f) for c, f in counts.items()]
    heapq.heapify(heap) 
    while len(heap) > 1:
        l, r = heapq.heappop(heap), heapq.heappop(heap)
        merged = HuffmanNode(None, l.freq + r.freq)
        merged.left, merged.right = l, r
        heapq.heappush(heap, merged)
    return heap[0]

def get_huffman_codes(node, code, mapping):
    if not node: return
    if node.char:
        mapping[node.char] = code
        return
    get_huffman_codes(node.left, code + "0", mapping)
    get_huffman_codes(node.right, code + "1", mapping)

# --- THE SHOWDOWN ---
def run_showdown():
    print("--- THE SHOWDOWN: Manual (Phase 1) vs. Huffman (Phase 2) ---")
    
    # Pathing logic
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file name (e.g., encoding_test.txt): ")
    # Going up 3 levels to reach /data
    file_path = os.path.join(base_dir, "..", "data", file_name)

    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. CALCULATE MANUAL (PHASE 1)
    counts = collections.Counter(text)
    sorted_chars = counts.most_common()
    manual_total_bits = 0
    for i, (char, count) in enumerate(sorted_chars):
        # Staircase logic: 1 bit for 1st, 2 for 2nd, 3 for 3rd...
        # Except the last one which stays the same length as the one before
        code_len = i + 1 if i < len(sorted_chars) - 1 else i
        if i == 0 and len(sorted_chars) == 1: code_len = 1
        manual_total_bits += (count * code_len)

    # 2. CALCULATE HUFFMAN (PHASE 2)
    root = build_tree(text)
    huff_mapping = {}
    get_huffman_codes(root, "", huff_mapping)
    huffman_total_bits = sum(counts[c] * len(huff_mapping[c]) for c in counts)

    # 3. RESULTS
    print("\n" + "="*40)
    print(f"FILE: {file_name}")
    print(f"Manual Staircase: {manual_total_bits} bits")
    print(f"Huffman Tree:      {huffman_total_bits} bits")
    print("-" * 40)
    
    diff = manual_total_bits - huffman_total_bits
    if diff > 0:
        print(f" Huffman is SHORTER by {diff} bits! 🏆")
    elif diff == 0:
        print(" It's a Tie! (Common for very simple text)")
    else:
        print("RESULT: Manual was somehow shorter (Mathematically impossible for large data!)")
    print("="*40)

if __name__ == "__main__":
    run_showdown()