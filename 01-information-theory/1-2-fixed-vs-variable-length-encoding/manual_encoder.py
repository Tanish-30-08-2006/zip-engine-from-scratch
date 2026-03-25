import os
import collections

def run_automatic_encoder():
    print("--- The Compression Lab: Automatic Variable-Length Encoder ---")

    #--------------------------READING DATA-----------------------#

    # File path 
    base_dir = os.path.dirname(__file__)
    file_name = input(F"Enter file name(from data folder) to fetch data from : (eg: complex.txt) :  ")
    file_path = os.path.join(base_dir,"..","data",file_name)

    # Does the file exists 
    if not os.path.exists(file_path):
        print(f"Error: The file '{filename}' was not found.")
        return
    
    with open(file_path,'r',encoding='utf-8') as file:
        file_content = file.read()
    
    if not file_content:
        print("Empty input! Try 'BEEP BOOP' or 'BANANA'")
        return
    
    #--------------------------FREQUENCY----------------------------#

    counts_per_char      = collections.Counter(file_content)
    total_chars          = len(file_content)

    # sort most frequent ---> least frequent
    # most frequent will be first in counts_per_char
    sorted_chars = counts_per_char.most_common()



    #-------------------------CODE ASSIGNMENT--------------------------#

    custom_dictionary = {}
    current_prefix = ""

    print("\n[Step 1] Generating Custom Dictionary:")
    print(f"{'Char':<10} | {'Count':<7} | {'New Binary Code'}")
    print("-" * 35)

    for i , (char,count) in enumerate(sorted_chars):
        
        if i == (len(sorted_chars) -1):
            # if it is very last (rarest) charzcter we dont need to write trailing 0's
            code = "1"*i if i>0 else "0"
        else:
            # create a string of 'i' ones followed by a '0'
            # Example: i=0 -> '0', i=1 -> '10', i=2 -> '110'
            code = ("1"*i) + "0"
        
        custom_dictionary[char] = code

        display_char = f"'{char}'" if char != " " else "Space"
        print(f"{display_char:<10} | {count:<7} | {code}")

    #--------------------------ENCODING WHOLE FILE CONTENT------------------------------#

    # We replace every character in the original text with our new code
    encoded_stream = ""
    
    for char in file_content:
        encoded_stream = encoded_stream + custom_dictionary[char]

    
    #------------------------DECODING ENCODED BIT CONTENT------------------------------------#

    # while decoding we need to lookup bits to find corresponding characters so flip the dictionary
    flipped_dict    = {bit_code: char for char , bit_code in custom_dictionary.items()}

    decoded_output = ""
    current_bits = "" # This is our "Accumulator" (memory)

    for bit in encoded_stream:
        current_bits = current_bits + bit

        if current_bits in flipped_dict:
            decoded_output = decoded_output + flipped_dict[current_bits]
            current_bits = ""


    #----------------------------------COMPARISON AND VERIFICATION-----------------------------------#

    ascii_size        = (total_chars)*(8)
    compressed_size   = len(encoded_stream)
    size_saved        = (1 - (compressed_size / ascii_size)) * 100

    print("-" * 50)
    print(f"Original Text:  {file_content[:30]}   ") 
    print(f"Decoded Text:   {decoded_output[:30]}   ")

    if file_content == decoded_output:
        print("VERIFICATION: SUCCESS! (Data is Lossless)")
    else:
        print("VERIFICATION: FAILED! (Data was corrupted)")

    print("\n The Resulting Bit-Stream:")
    print(f"Binary: {encoded_stream}") 
    
    print("\n Final Efficiency Audit:")
    print(f"Original Size (ASCII 8-bit): {ascii_size} bits")
    print(f"New Compressed Size:         {compressed_size} bits")
    print(f"Space Saved:                 {size_saved:.2f}%")



if __name__ == "__main__":
    run_automatic_encoder()
    
    
