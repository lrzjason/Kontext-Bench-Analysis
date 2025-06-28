import json

def extract_instructions(input_jsonl_path, output_txt_path):
    try:
        with open(input_jsonl_path, 'r', encoding='utf-8') as infile, \
             open(output_txt_path, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                try:
                    data = json.loads(line)
                    if 'instruction' in data:
                        outfile.write(data['instruction'] + '\n')
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line.strip()}")
                except Exception as e:
                    print(f"An error occurred processing a line: {e}")
        print(f"Successfully extracted instructions to {output_txt_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_jsonl_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    input_file = 'metadata.jsonl'
    output_file = 'instructions.txt'
    extract_instructions(input_file, output_file)

