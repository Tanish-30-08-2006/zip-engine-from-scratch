# The Encoder: Uses Frequency --> Tree --> Lengths --> Header String.   
# The File: Saves the Header String + Encoded Bits.
# The Decoder: Reads Header String --> Calculates Codes --> Decodes Bits.

import collections
import heapq
import os

class HuffmanNode:
    """ The building block for Tree """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Allows heapq to sort nodes based on frequency
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(content):
    
    #--------------------COUNT FREQ OF CHAR AND CREATE PRIORITY QUEUE---------------#
    counts = collections.Counter(content)

    # create a list of leaf nodes [ each item in heap is huffmannode object ]
    heap = [HuffmanNode(char,freq) for char , freq in counts.items()]

    # Transforming  list into a 'Min-Heap' (Priority Queue)
    # Now, heap[(0] will ALWAYS be the smallest frequency node
    heapq.heapify(heap)

    #-----------------MERGING TWO LEAST FREQ CHARACTERS TO BRANCH RECURSIVELY TO FIND ROOT------#

    while len(heap) > 1 :
        # Pop the two smallest nodes..
        node_left  = heapq.heappop(heap) 
        node_right = heapq.heappop(heap)

        # creating a branch ( only freq as sum no char)
        merged_parent = HuffmanNode(None, node_left.freq + node_right.freq)
        merged_parent.left = node_left
        merged_parent.right = node_right

        # Push the parent back into the heap to be merged again later
        heapq.heappush(heap,merged_parent)
    
    # last node remaining will be root of the entire tree
    return heap[0]

def generate_codes(node, current_code, huffman_codes):
    """ Walking the tree to find the bit-paths """
    if node is None:
        return
    
    # if we reached a leaf i.e node with a character
    if node.char is not None:
        huffman_codes[node.char] = current_code
        return
    
    # Walk Left (add '0') and Walk Right (add '1')
    generate_codes(node.left, current_code + "0", huffman_codes)
    generate_codes(node.right, current_code + "1", huffman_codes)

def run_huffman_lab():
    print("--- Phase 2: The Huffman Engine ---")

    #--------------READING DATA-----------------------#

    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file to compress (e.g., encoding_test.txt): ")
    file_path = os.path.join(base_dir, "..","data", file_name)

    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build the huffman tree
    root_node = build_huffman_tree(content)

    # Extract codes from the tree
    huffman_codes = {}
    generate_codes(root_node, "", huffman_codes)

    print(f"\n[Huffman Dictionary for {file_name}]:")
    print(f"{'Char':<10} | {'Huffman Code':<15}")
    print("-" * 30)
    for char in sorted(huffman_codes, key=lambda x: len(huffman_codes[x])):
        display_char = f"'{char}'" if char != " " else "Space"
        print(f"{display_char:<10} | {huffman_codes[char]:<15}")

    # 4. Final Efficiency Check
    encoded_bits = "".join([huffman_codes[c] for c in content])
    ascii_bits = len(content) * 8
    print(f"\nOriginal (8-bit): {ascii_bits} bits")
    print(f"Huffman Encoded:  {len(encoded_bits)} bits")
    print(f"Compression:      {(1 - len(encoded_bits)/ascii_bits):.2%}")

if __name__ == "__main__":
    run_huffman_lab()