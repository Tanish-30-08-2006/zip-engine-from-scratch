# -*- coding: utf-8 -*-
import os

class BitPacker:
    """
    The 'Funnel' that turns Huffman bit-strings into 8-bit Bytes.
    """
    def __init__(self):
        self.current_byte = 0  # Our 8-bit 'Bucket'
        self.bits_filled = 0   # How many slots in the bucket are used
        self.output_bytes = bytearray() # The final list of bytes to save

    def push_bits(self, bit_string):
        """
        Takes a string like '1101' and pours it into 8-bit buckets.
        """
        for bit in bit_string:
            # 1. Convert the character '1' or '0' into an actual integer
            bit_val = int(bit)

            # 2. SHIFT: Make room at the 'right side' of our bucket
            # Example: 00000101 becomes 00001010
            self.current_byte <<= 1
            
            # 3. GLUE: Place the bit into the new empty slot
            # Example: 00001010 | 1 becomes 00001011
            self.current_byte |= bit_val
            
            # 4. TRACK: Update how many slots we've used
            self.bits_filled += 1

            # 5. OVERFLOW CHECK: Is the bucket full (8 bits)?
            if self.bits_filled == 8:
                # Add this full byte to our collection
                self.output_bytes.append(self.current_byte)
                
                # RESET: Start a fresh empty bucket
                self.current_byte = 0
                self.bits_filled = 0

    def flush(self):
        """
        If we finished the file but the last bucket isn't full (e.g., 3 bits used),
        we 'pad' it with zeros to make it a full 8-bit byte.
        """
        if self.bits_filled > 0:
            # Shift the remaining bits to the left to fill the byte
            padding_needed = 8 - self.bits_filled
            self.current_byte <<= padding_needed
            self.output_bytes.append(self.current_byte)
            
            # Reset
            self.current_byte = 0
            self.bits_filled = 0
        
        return self.output_bytes

# -------------------------------------------------------------------------
# THE PHYSICAL LABORATORY RUNNER
# -------------------------------------------------------------------------

def run_bit_packing_lab():
    print("\n" + "="*60)
    print("      PHASE 4.1: THE BIT-PACKING (PHYSICAL STORAGE)      ")
    print("="*60)

    # Simulation: Let's assume DEFLATE gave us these Huffman bits
    # 'A' = 110, 'B' = 01, 'C' = 1111
    bit_stream = "110011111" 
    print(f"\n[Input] Huffman Bitstream: {bit_stream}")
    print(f"Logic: This looks like 9 bits. It should result in 2 Bytes.")

    # --- EXECUTION ---
    packer = BitPacker()
    packer.push_bits(bit_stream)
    packed_data = packer.flush()

    # --- THE REVEAL ---
    print("\n[Output] Physical Bytes Generated:")
    print("-" * 45)
    for i, b in enumerate(packed_data):
        # bin(b) shows the binary, zfill(8) ensures we see all 8 slots
        print(f"Byte {i}: {bin(b)[2:].zfill(8)} (Hex: {hex(b)}, Decimal: {b})")
    print("-" * 45)

    # --- SAVING TO DISK ---
    output_path = "compressed_test.bin"
    with open(output_path, "wb") as f:
        f.write(packed_data)
    
    print(f"\nSUCCESS: Created '{output_path}'")
    print(f"Original Bit-String length: {len(bit_stream)} 'text' chars")
    print(f"Physical file size: {len(packed_data)} actual bytes")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_bit_packing_lab()