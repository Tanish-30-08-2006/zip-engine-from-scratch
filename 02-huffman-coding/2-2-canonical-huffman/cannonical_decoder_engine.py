# -*- coding: utf-8 -*-
import heapq
import collections
import os

# -------------------------------------------------------------------------
# PART 1: THE BUILDING BLOCKS (THE NODE)
# -------------------------------------------------------------------------

class HuffmanNode:
    """ 
    Standard Node for initial Tree construction.
    We use this just to calculate how many bits each character NEEDS.
    """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # This allows the Priority Queue (heapq) to sort nodes by their frequency
    def __lt__(self, other):
        return self.freq < other.freq


# -------------------------------------------------------------------------
# PART 2: THE STANDARD TREE LOGIC (FINDING BIT-LENGTHS)
# -------------------------------------------------------------------------

def build_standard_tree(text):
    """ Builds a normal Huffman tree to determine optimal bit-depths """
    counts = collections.Counter(text)
    
    # Create the 'Forest' of leaf nodes
    heap = [HuffmanNode(c, f) for c, f in counts.items()]
    heapq.heapify(heap)

    # Merge nodes until only the Root remains
    while len(heap) > 1:
        left_child = heapq.heappop(heap)
        right_child = heapq.heappop(heap)
        
        # Create a parent with no character, just the sum of frequencies
        merged = HuffmanNode(None, left_child.freq + right_child.freq)
        merged.left = left_child
        merged.right = right_child
        
        heapq.heappush(heap, merged)
        
    return heap[0] # Returns the top-most node (The Root)


def get_bit_lengths(node, current_depth, lengths_dict):
    """ 
    Recursively walks the tree. 
    We don't care about the '0' and '1' paths here.
    We ONLY care about how DEEP (how many bits) each character is.
    """
    if node is None:
        return
    
    # If we reached a leaf (actual character)
    if node.char is not None:
        lengths_dict[node.char] = current_depth
        return
    
    # Keep walking down
    get_bit_lengths(node.left, current_depth + 1, lengths_dict)
    get_bit_lengths(node.right, current_depth + 1, lengths_dict)


# -------------------------------------------------------------------------
# PART 3: THE CANONICAL LOGIC (REBUILDING THE DICTIONARY)
# -------------------------------------------------------------------------

def generate_canonical_codes(lengths_dict):
    """
    THE SYSTEM DESIGN MASTERPIECE:
    This recreates the codes using ONLY the bit-lengths.
    It follows the standard ZIP rule: Sort by length, then by Alphabet.
    """
    
    # 1. Sort the characters: 
    # Primary sort: Bit Length (x[1])
    # Secondary sort: The Character itself (x[0]) for alphabetical order
    sorted_items = sorted(lengths_dict.items(), key=lambda x: (x[1], x[0]))

    canonical_map = {}
    current_code_value = 0
    last_bit_length = sorted_items[0][1] # Start with the shortest length found

    for char, length in sorted_items:
        
        # LOGIC: If the bit-length increases (e.g. from a 2-bit code to a 3-bit code)
        # we must 'Shift Left' the binary value to preserve the Prefix Property.
        while last_bit_length < length:
            current_code_value <<= 1  # Binary shift left: 10 (2) becomes 100 (4)
            last_bit_length += 1
        
        # Convert the integer value to a binary string padded with 0s to 'length'
        # e.g. If code is 1 and length is 3, format creates "001"
        binary_string = format(current_code_value, '0' + str(length) + 'b')
        canonical_map[char] = binary_string
        
        # Increment for the next character in this length group
        current_code_value += 1

    return canonical_map


# -------------------------------------------------------------------------
# PART 4: THE LAB EXECUTION
# -------------------------------------------------------------------------

def run_canonical_lab():
    print("\n" + "="*50)
    print("   PHASE 2.2: THE CANONICAL HUFFMAN ENGINE   ")
    print("="*50)

    # Path Setup
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file name (e.g., encoding_test.txt): ")
    
    # Move up levels to find the 'data' folder
    # Adjust levels depending on your exact folder depth
    file_path = os.path.join(base_dir, "..", "data", file_name)

    if not os.path.exists(file_path):
        print(f"\n[!] Error: File '{file_path}' not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- EXECUTION FLOW ---

    # 1. Get the Bit-Lengths using a standard tree
    print("\n[Step 1] Analyzing Information Density...")
    root = build_standard_tree(content)
    lengths_dict = {}
    get_bit_lengths(root, 0, lengths_dict)

    # 2. Convert those lengths into a Canonical Map
    # This is the map that can be reconstructed with NO tree data!
    print("[Step 2] Transforming to Canonical Form...")
    canonical_dict = generate_canonical_codes(lengths_dict)

    # 3. Display the results for GitHub Insights
    print("\n[Step 3] Canonical Header Result:")
    print("-" * 55)
    print(f"{'Character':<12} | {'Bit-Length':<12} | {'Canonical Code'}")
    print("-" * 55)

    # Sort alphabetially for the final display
    for char in sorted(canonical_dict.keys()):
        display_char = f"'{char}'" if char != " " else "Space"
        code = canonical_dict[char]
        print(f"{display_char:<12} | {len(code):<12} | {code}")

    print("-" * 55)
    print("\nSUMMARY: To decode this, a ZIP file ONLY needs to save")
    print("the 'Bit-Length' column. The tree structure is now math!")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_canonical_lab()