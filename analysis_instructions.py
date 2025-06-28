

import json
from collections import Counter
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

def analyze_instructions(input_jsonl_path, output_md_path):
    instructions = []
    try:
        with open(input_jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if 'instruction' in data:
                        instructions.append(data['instruction'])
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_jsonl_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    if not instructions:
        print("No instructions found in the file.")
        return

    # Preprocessing
    cleaned_instructions = [clean_text(inst) for inst in instructions]
    words = [word for inst in cleaned_instructions for word in inst.split()]

    # Frequency Analysis
    word_counts = Counter(words)

    bigrams = []
    for inst in cleaned_instructions:
        tokens = inst.split()
        if len(tokens) >= 2:
            bigrams.extend([f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)])
    bigram_counts = Counter(bigrams)

    trigrams = []
    for inst in cleaned_instructions:
        tokens = inst.split()
        if len(tokens) >= 3:
            trigrams.extend([f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}" for i in range(len(tokens)-2)])
    trigram_counts = Counter(trigrams)

    # Structure Analysis (Basic - First word)
    first_words = [inst.split()[0] for inst in cleaned_instructions if inst.split()]
    first_word_counts = Counter(first_words)

    # Output to Markdown
    try:
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write("# Instruction Analysis Results\n\n")

            f.write("## Top 20 Most Frequent Words\n")
            for word, count in word_counts.most_common(20):
                f.write(f"- {word}: {count}\n")
            f.write("\n")

            f.write("## Top 20 Most Frequent Bigrams\n")
            for bigram, count in bigram_counts.most_common(20):
                f.write(f"- {bigram}: {count}\n")
            f.write("\n")

            f.write("## Top 20 Most Frequent Trigrams\n")
            for trigram, count in trigram_counts.most_common(20):
                f.write(f"- {trigram}: {count}\n")
            f.write("\n")

            f.write("## Common Instruction Structures (First Word)\n")
            for word, count in first_word_counts.most_common(10):
                f.write(f"- {word}: {count}\n")
            f.write("\n")

            f.write("## Summary of Observations\n")
            f.write("This section would contain a more detailed summary of common patterns, verbs, and phrases identified from the frequency analyses.\n")

        print(f"Analysis complete. Results saved to {output_md_path}")

    except Exception as e:
        print(f"An error occurred while writing the output file: {e}")

if __name__ == "__main__":
    input_file = "metadata.jsonl"
    output_file = "analysis.md"
    analyze_instructions(input_file, output_file)

