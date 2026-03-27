# -*- coding: utf-8 -*-

class ArchivePacker:
    """
    The Professional Bit-Packer that handles Headers + Data.
    """
    def __init__(self):
        self.byte_accumulator = bytearray()
        self.current_byte = 0
        self.bits_in_bucket = 0

    def add_byte_directly(self, byte_val):
        """
        Sometimes we don't want to pack bits, we just want to 
        slam a whole character (like 'P') into the file.
        """
        # We must flush any partial bits first to keep alignment!
        self.flush_bits()
        self.byte_accumulator.append(byte_val)

    def add_bits(self, bit_string):
        """
        The 'Funnel' logic from before - for Huffman codes.
        """
        for bit in bit_string:
            self.current_byte = (self.current_byte << 1) | int(bit)
            self.bits_in_bucket += 1
            if self.bits_in_bucket == 8:
                self.byte_accumulator.append(self.current_byte)
                self.current_byte = 0
                self.bits_in_bucket = 0

    def flush_bits(self):
        """ Completes the current byte with zeros if needed """
        if self.bits_in_bucket > 0:
            self.current_byte <<= (8 - self.bits_in_bucket)
            self.byte_accumulator.append(self.current_byte)
            self.current_byte = 0
            self.bits_in_bucket = 0

# -------------------------------------------------------------------------
# THE GENERALIZED FLOW (Step-by-Step)
# -------------------------------------------------------------------------

def create_generalized_archive_demo():
    packer = ArchivePacker()

    print("\n" + "="*60)
    print("      PHASE 4.1: BUILDING THE GENERALIZED HEADER      ")
    print("="*60)

    # STEP 1: THE MAGIC HANDSHAKE
    print("[Step 1] Writing Magic Bytes: 'P' and 'K'...")
    packer.add_byte_directly(ord('P')) # 0x50
    packer.add_byte_directly(ord('K')) # 0x4B

    # STEP 2: THE FILENAME
    filename = "lab_results.bin"
    print(f"[Step 2] Packing Filename: '{filename}'")
    # We write the length of the name first so decoder knows when the name ends
    packer.add_byte_directly(len(filename)) 
    for char in filename:
        packer.add_byte_directly(ord(char))

    # STEP 3: THE HUFFMAN MAP (Simulation)
    # Let's say we have a symbol 'A' with a 3-bit Huffman code
    print("[Step 3] Packing Huffman Table Metadata...")
    # In a real one, we'd loop through our Canonical Table here
    packer.add_bits("110") # The code for 'A'
    
    # STEP 4: FINALIZING
    packer.flush_bits()
    final_data = packer.byte_accumulator

    print("\n[Result] Physical Archive Construction Complete.")
    print("-" * 45)
    print(f"Total Bytes in File: {len(final_data)}")
    print(f"Header Signature: {final_data[0:2].decode('ascii')}")
    print("-" * 45)

if __name__ == "__main__":
    create_generalized_archive_demo()