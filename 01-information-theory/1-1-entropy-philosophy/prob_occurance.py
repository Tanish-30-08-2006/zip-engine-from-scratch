import collections # this helps to count things easily  
import math        # needed for information theory math later 

def analyze_data_dna():
    print("--- The Compression Lab: Step 1.1 ---")

    while True:
        user_input = input("enter text to analyse or type 'quit' ")
        
        if user_input.lower() =='quit':
            print("Exiting entropy calculation lab..")
            break

        if not user_input:
            print("please enter some text to analyse :")
            continue

        total_chars = len(user_input)
        char_counts = collections.Counter(user_input)

        print(f"\nAnalysis for: '{user_input}'")
        print(f"Total Characters (Bytes): {total_chars}")
        print(f"{'Char':<10} | {'Count':<10} | {'Probability':<12} | {'Status'}")
        print("-" * 50)

        for character , count in char_counts.items():
            prob = count/total_chars

            if prob>0.4 :
                status = "High Rebundancy"
            else:
                status = "Low Rebundancy"

            display_char = f"'{character}'" if character != " " else "'Space'"
            
            print(f"{display_char:<10} | {count:<10} | {prob:<12.2%} | {status}")

        unique_chars = len(char_counts)
        print("-" * 50)
        print(f"Unique Characters: {unique_chars}")

        if unique_chars == 1:
            print("Verdict: This is 100% predictable. Extreme compression possible!")
        elif unique_chars == total_chars:
            print("Verdict: Every character is unique. This is high-entropy (hard to compress).")
        else:
            print(f"Verdict: Found {total_chars - unique_chars} redundant instances. Ready for compression logic.")



# this line tells python run the function analyze_data_dna() when the file is executed as python creates
# a special variable __name__ and sets it to "__main__" when the file is run as a script
# otherwise it sets it to the name of the module as it is imported for example if we import this file in another file
# then __name__ will be "entropy_calc" and not "__main__"  also this is a good practice to use this 
# when we  are writing code that can be run as a script or imported as a module thus we can use the same code 
# in different ways for example we can import this file in another file and use the function analyze_data_dna() 
# in that file
 
if __name__ == "__main__":
    analyze_data_dna()                              