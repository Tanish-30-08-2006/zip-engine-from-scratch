# -*- coding: utf-8 -*-
import os
import collections

# -------------------------------------------------------------------------
# PART 1: THE GENERALIZED SYMBOLIZER (LZ77 CORE)
# -------------------------------------------------------------------------

def calculate_compression_stats(symbols, original_text_len):
    """
    Calculates how many characters were 'absorbed' by matches 
    versus how many literals remain.
    """
    chars_covered_by_matches = sum(s["len"] for s in symbols if s["type"] == "MATCH")
    total_literals = sum(1 for s in symbols if s["type"] == "LITERAL")
    
    # How much did LZ77 shrink the 'raw' character count?
    lz77_reduction_pct = (chars_covered_by_matches / original_text_len) * 100
    
    return {
        "match_coverage": chars_covered_by_matches,
        "literal_count": total_literals,
        "reduction": lz77_reduction_pct,
        "symbol_count": len(symbols)
    }

def get_deflate_symbols(text, window_size=32768, min_match=3):
    """
    Scans text and decides: Is this a single letter (LITERAL) or a repeat (MATCH)?
    """
    symbols = []
    cursor = 0
    
    while cursor < len(text):
        best_dist = 0
        best_len = 0
        
        # 1. SEARCHING THE PAST (The Sliding Window)
        search_start = max(0, cursor - window_size)
        
        for start_pos in range(search_start, cursor):
            curr_len = 0
            while (cursor + curr_len < len(text) and 
                   text[start_pos + curr_len] == text[cursor + curr_len]):
                curr_len += 1
            
            if curr_len > best_len:
                best_len = curr_len
                best_dist = cursor - start_pos

        # 2. DECISION LOGIC
        if best_len >= min_match:
            # We found a repeat! Store the Distance and Length
            # We also store the 'raw_text' just for the display section later
            matched_text = text[cursor : cursor + best_len]
            symbols.append({
                "type": "MATCH", 
                "dist": best_dist, 
                "len": best_len,
                "raw": matched_text
            })
            cursor += best_len
        else:
            # No repeat found, keep it as a single character
            symbols.append({
                "type": "LITERAL", 
                "value": text[cursor]
            })
            cursor += 1
            
    symbols.append({"type": "END", "value": "END_MARKER"})
    return symbols

# -------------------------------------------------------------------------
# PART 2: THE INFORMATIVE LAB RUNNER
# -------------------------------------------------------------------------

def run_deflate_lab():
    print("\n" + "="*70)
    print("      PHASE 3.2: DEFLATE ENGINE - THE SYMBOLIZER TRACER      ")
    print("="*70)

    # Path Logic
    base_dir = os.path.dirname(__file__)
    file_name = input("Enter file (e.g., repetitive.txt): ")
    file_path = os.path.join(base_dir, "..", "data", file_name)

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- EXECUTION ---
    print(f"\n[Step 1] Processing '{file_name}' ({len(content)} chars)...")
    symbols = get_deflate_symbols(content, window_size=500)

    # --- NEW INFORMATIVE DISPLAY SECTION ---
    print("\n[Step 2] How the Symbols were Generated (First 15 steps):")
    print("-" * 70)
    print(f"{'Type':<10} | {'Content / Info':<30} | {'Resulting Symbol'}")
    print("-" * 70)

    for s in symbols[:15]: # Trace the first 15 decisions
        if s["type"] == "LITERAL":
            char_display = f"'{s['value']}'" if s['value'] != " " else "Space"
            print(f"{'LITERAL':<10} | {char_display:<30} | {s['value']}")
        elif s["type"] == "MATCH":
            info = f"Found '{s['raw']}' at Dist {s['dist']}"
            sym = f"L{s['len']}_D{s['dist']}"
            print(f"{'MATCH':<10} | {info:<30} | {sym}")
        else:
            print(f"{'END':<10} | {'Reached End of Block':<30} | [256]")

    # --- FREQUENCY AUDIT ---
    print("\n" + "-" * 70)
    print("[Step 3] Frequencies for Huffman (The 'Super Alphabet'):")
    
    freq_map = collections.Counter()
    for s in symbols:
        if s["type"] == "LITERAL": freq_map[s["value"]] += 1
        elif s["type"] == "MATCH": freq_map[f"LEN_{s['len']}"] += 1
    
    print(f"Top 5 Most Frequent Symbols:")
    for sym, count in freq_map.most_common(5):
        print(f"  > {str(sym):<10} appeared {count} times")

    # --- SUMMARY ---
    match_chars = sum(s["len"] for s in symbols if s["type"] == "MATCH")
    literal_chars = sum(1 for s in symbols if s["type"] == "LITERAL")
    
    # --- ENHANCED FINAL ANALYSIS ---
    stats = calculate_compression_stats(symbols, len(content))
    
    print("\n" + "="*70)
    print("      📈 FINAL DEFLATE EFFICIENCY REPORT (LZ77 PHASE)      ")
    print("="*70)
    print(f"{'Metric':<35} | {'Value'}")
    print("-" * 70)
    print(f"{'Original File Size':<35} | {len(content)} Bytes/Chars")
    print(f"{'Characters Eaten by Matches':<35} | {stats['match_coverage']}")
    print(f"{'Remaining Literals (Unique)':<35} | {stats['literal_count']}")
    print(f"{'Total Symbols for Huffman Tree':<35} | {stats['symbol_count']}")
    print("-" * 70)
    print(f"{'LZ77 Compression Efficiency':<35} | {stats['reduction']:.2f}%")
    print("-" * 70)
    
    print("\n[Educational Insight]:")
    if stats['reduction'] > 50:
        print("💡 EXCELLENT: This file has high redundancy. LZ77 did the heavy lifting!")
    else:
        print("💡 NOTE: Low redundancy. Huffman will need to work harder on individual bits.")
    
    print("\nNEXT STEP: We will now turn these symbols into a Huffman Tree.")
    print("A 'MATCH' symbol will take the same 'space' as a single character 'A'.")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_deflate_lab()