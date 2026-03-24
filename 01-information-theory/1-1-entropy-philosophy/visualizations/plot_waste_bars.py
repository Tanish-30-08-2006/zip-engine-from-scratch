import os
import math
import collections
import matplotlib.pyplot as plt


def run_waste_visualization():
    print("--- The Compression Lab: Visualization 2 ---")

    #-------------------------------READING DATA FROM FILE-----------------#
    base_dir = os.path.dirname(__file__)
    file_name = input ("Enter file name to analyze (e.g., repetitive.txt): ")
    file_path = os.path.join(base_dir,"..","..","data",file_name)

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content:
        print("File is empty!")
        return
    
    #----------------------------------------LOGIC-----------------------------------------#

    counts = collections.Counter(content)
    total_chars = len(content)

    chars = []
    shannon_values = []
    ascii_values = []

    # sorting characters by frequency so graph looks organised highest to lowest
    sorted_chars = counts.most_common()

    for char, count in sorted_chars:
        p =( count) /( total_chars)
        ideal = -math.log2(p)
        
        display_name = f"'{char}'" if char != " " else "Space"
        
        chars.append(display_name)
        ascii_values.append(8.0)      # always 8 bits for every character by ascii or utf-8 encoding schemes
        shannon_values.append(ideal)  # ideal bits of information needed for character by -log2(prob of occurance)
    
    #---------------------------PLOTTING BAR CHART----------------------------------------#

    plt.figure(figsize=(10,6))

    # we will use index to place bars side by side
    index = range(len(chars))
    bar_width = 0.35

    # plt.bar syntax ----> plt.bar( X , Y , width , label , color )

    # FIRST BAR : ASCII STANDARD ( 8 BITS )
    plt.bar(index, ascii_values , bar_width, label='Current (ASCII 8-bit)', color='gray', alpha=0.5)

    # SECOND BAR : SHANNON LIMIT (IDEAL GOAL TO ACHIEVE)
    # shift x by barwidth for every index for two bars to be side by side 
    plt.bar([i + bar_width for i in index], shannon_values ,bar_width , label='Ideal (Shannon Limit)', color='green')

    # labels
    plt.title(f"Wasted Bits per Character Analysis: {file_name}")
    plt.xlabel("Characters found in file")
    plt.ylabel("Cost in Bits")

    # plt.xticks puts the character names ('a', 'b', etc.) under the bars
    plt.xticks([i + bar_width/2 for i in index], chars)

    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)  

    # --------------------------SAVING THE OUTPUT----------------------#

    base_dir = os.path.dirname(__file__)
    output_folder = os.path.join(base_dir, "..", "..","data", "output", "images")
    curve_image_path = os.path.join(output_folder, "waste_bits_per_character_bar_.png")

    if not os.path.exists(output_folder):
        print(f"Error: The folder '{output_folder}' does not exist.")
        print("Please manually create 'data/output/images/' at the project root.")
        return
    
    plt.savefig(curve_image_path)

    plt.close()

    








if __name__ == "__main__":
    run_waste_visualization()
