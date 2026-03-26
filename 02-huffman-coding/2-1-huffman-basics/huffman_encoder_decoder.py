# The Encoder: Uses Frequency --> Tree --> Lengths --> Header String.   
# The File: Saves the Header String + Encoded Bits.
# The Decoder: Reads Header String --> Calculates Codes --> Decodes Bits.

import heapq
import os
import collections

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Allows heapq to sort nodes by frequency
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    """ Builds the physical tree structure using a Priority Queue """
    counts = collections.Counter(text) 
    
    # Create leaf nodes and push into heap
    heap = [HuffmanNode(char, freq) for char, freq in counts.items()]
    heapq.heapify(heap) # <FIX>: Corrected syntax

    while len(heap) > 1:
        node_left = heapq.heappop(heap)
        node_right = heapq.heappop(heap)

        # Create parent (internal node)
        merged = HuffmanNode(None, node_left.freq + node_right.freq)
        merged.left = node_left
        merged.right = node_right
        
        heapq.heappush(heap, merged)

    return heap[0] # Return the Root

def get_codes(node, current_code, mapping):
    """ Recursive function to extract bits from the tree for Encoding """
    if not node:
        return
    if node.char is not None:
        mapping[node.char] = current_code
        return
    get_codes(node.left, current_code + "0", mapping)
    get_codes(node.right, current_code + "1", mapping)

def decode_bits(root, bit_stream):
    """ 
    THE TREE-WALKER: 
    Translates bits back to text by physically moving through the tree nodes.
    """
    decoded_text = ""
    current_node = root # Start at the top (Entrance)

    for bit in bit_stream:
        # Move Left for 0, Right for 1
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        # Check: Have we reached a Leaf
        if current_node.char is not None:
            decoded_text += current_node.char # Found a letter!
            current_node = root # move back to the top for the next letter

    return decoded_text

def run_huffman_lab():
    print("--- Phase 2: Complete Huffman Encoder/Decoder ---")

    # 1. SETUP & PATHING
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file (e.g., encoding_test.txt): ")
    # Up 3 levels to reach project root /data
    file_path = os.path.join(base_dir, "..",  "data", file_name)

    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    # 2. ENCODING PHASE
    tree_root = build_huffman_tree(original_text)
    huff_codes = {}
    get_codes(tree_root, "", huff_codes)
    
    encoded_bits = "".join([huff_codes[c] for c in original_text])

    # 3. DECODING PHASE (The New Logic)
    decoded_text = decode_bits(tree_root, encoded_bits)

    # 4. FINAL VERIFICATION
    print("\n" + "="*50)
    print(f"Encoded Bits:  {encoded_bits[:50]}   ")
    print(f"Decoded Text:  {decoded_text[:50]}   ")
    
    if original_text == decoded_text:
        print("\nVERIFICATION: SUCCESS :  (100% Lossless)")
    else:
        print("\nVERIFICATION: FAILED (Data Corrupted)")
    
    # Calculate Savings
    saved = (1 - (len(encoded_bits) / (len(original_text)*8))) * 100
    print(f"Space Saved:   {saved:.2f}%")
    print("="*50)

if __name__ == "__main__":
    run_huffman_lab()