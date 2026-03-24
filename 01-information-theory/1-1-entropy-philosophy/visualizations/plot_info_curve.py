import numpy as np
import matplotlib.pyplot as plt
import os



def run_visualization():
    print("--- The Compression Lab: Visualization 1 ---")
    print("Generating the 'Probability vs. Information' curve...")

    # -----------------------NUMPY DATA GENERATION---------------------------------------------
    # Numpy data generation : to plot X,Y (prob vs info) we need thousands of points
    # of probabilites and corresponding information we cant plot a smooth curve with just 3 or 4 points
    # like p=0.1 0.2 ... 1.0 we cant plot a smooth curve from this and take insights we need thousands of 
    # points for smooth plot 
    

    # NUMPY SYNTAX FOR DATA GENERATION
    # np.linspace(start , stop , number_of_points) creates a list of evenly spaced numbers 
    # np.linspace = np.linearspace 

    probabilities_list = np.linspace(0.001,1,1000)

    information_bits_list = -np.log2(probabilities_list)

    

    # ---------------PLOTTING GRAPH-------------#

    plt.figure(figsize=(8,5))

    plt.plot(probabilities_list,information_bits_list,color='blue',linewidth =2.5,label = 'Shannon Information Limit')

    plt.title("Visual Proof: Rare Events Carry More Information")

    plt.xlabel("Probability of Character (P)")
    plt.ylabel("Surprise / Information Cost (bits)")

    plt.grid(True,alpha=0.3)

    plt.legend()

    # ----------------PATH FOR SAVING THE OUTPUT-------------#

    base_dir = os.path.dirname(__file__)
    output_folder = os.path.join(base_dir, "..", "..","data", "output", "images")
    curve_image_path = os.path.join(output_folder, "information_curve.png")

    if not os.path.exists(output_folder):
        print(f"Error: The folder '{output_folder}' does not exist.")
        print("Please manually create 'data/output/images/' at the project root.")
        return
    
    plt.savefig(curve_image_path)

    plt.close()


if __name__ == "__main__":
    run_visualization()

