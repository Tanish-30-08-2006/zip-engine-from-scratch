
class HuffmanNode: 
    """
    The building block of our Huffman Tree.
    """

    def __init__(self,char,freq):
        self.char  = char         # None if its a branch as branch is just sum of frequencies of two leaf nodes 
        self.freq  = freq
        self.left  = None         # '0' bit  node on the left 
        self.right = None         # '1' bit  node on the right

    # this special function helps python compare frequencies of two nodes to put on left or right 
    def __lt__(self,other):
        return self.freq < other.freq
    
    def build_simple_tree_manual():
        """
        Let's manually build a tree for "ABB" to see the logic.
        Counts: A=1, B=2
        """

        print("--- Huffman Logic: Manual Tree Construction ---")

        # create leaf nodes for our characters ..(characters will only have leaf nodes as branch will not have character)
        node_a = HuffmanNode("A",1)
        node_b = HuffmanNode("B", 2)

        # MERGE : we created two nodes and merge it to create a parent 'Branch'
        # The parent's frequency is the SUM of its children (1 + 2 = 3)

        root = HuffmanNode( None,(node_a.freq + node_b.freq))
        root.left = node_a  # Higher freq goes to the left and lower on right
        root.right = node_b # Path '0' leads to "A" (higher) and '1' to "B" (lower) 

        print(f"Root Frequency: {root.freq}")
        print(f"Left Child: {root.left.char} (Freq: {root.left.freq})")
        print(f"Right Child: {root.right.char} (Freq: {root.right.freq})")

        # 3. GENERATE CODES (Walking the tree)
        # If we go left, code is '0'. If we go right, code is '1'.
        codes = {"A": "0", "B": "1"}
        print(f"\nResulting Codes: {codes}")

if __name__ == "__main__":
    build_simple_tree_manual()


