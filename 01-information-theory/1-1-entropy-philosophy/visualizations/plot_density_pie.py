import os
import math 
import collections
import matplotlib.pyplot as plt

def run_density_visualization():
    print("--- The Compression Lab: Visualization 3 ---")

    #------------------------------DATA READING ---------------------------#
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file name for final audit (e.g., repetitive.txt): ")
    file_path = os.path.join(base_dir,"..","..","data",file_name)

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    with open(file_path ,"r",encoding='utf-8') as f:
        content = f.read()
    
    

    counts_per_char = collections.Counter(content)
    entropy_sum     = 0
    total_chars     = len(content)

    #---------CALCULATING ENTROPY (AVG OF INFORMATION)-------------------#

    for count in counts_per_char.values():
        p = (count)/(total_chars)
        info = (-1)*(math.log2(p))
        entropy_sum = entropy_sum + (p)*(info)
    
    actual_information_total_bits = (entropy_sum)*(total_chars)
    total_file_size_bits = len(content)*(8) # 8 bits allocated for every character , symbol , sign.

    wasted_total_bits = (total_file_size_bits) - (actual_information_total_bits)

    density_percentage = (actual_information_total_bits / total_file_size_bits)


    #----------------------PLOTTING THE PIE CHART------------------------#

    data_points = [actual_information_total_bits, wasted_total_bits]
    data_labels = ['Useful Info', 'Wasted Bits Storage']
    data_colors = ['#2E8B57', '#F08080']

    plt.figure(figsize=(7,7))
    explode_logic = (0.1, 0)
    
    # plt.pie( data points , labels , colors , autopct = %1.1f%%) autopct calculates perrcentage on each slice and print it 
    plt.pie(data_points, labels=data_labels, colors=data_colors, autopct='%1.1f%%',explode=explode_logic,shadow=True,startangle=140)

    plt.title(f"Final Audit: Information Density of '{file_name}'")

    plt.figtext(0.5, 0.05, f"Information Density: {density_percentage:.2%}", ha="center", fontsize=12, fontweight='bold')

    #--------------------SAVING THE OUTPUT--------------------------#

    output_folder = os.path.join(base_dir, "..", "..","data", "output", "images")
    curve_image_path = os.path.join(output_folder, "Density_info_vs_waste_pie.png")

    if not os.path.exists(output_folder):
        print(f"Error: The folder '{output_folder}' does not exist.")
        print("Please manually create 'data/output/images/' at the project root.")
        return
    
    plt.savefig(curve_image_path)

    plt.close()
    print(f"SUCCESS: Density pie chart saved to: {curve_image_path}")

if __name__ =="__main__":
    run_density_visualization()
    

    
    
    
