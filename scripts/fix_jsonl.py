"""
Fix JSONL files that have all records on one line.

Splits improperly formatted JSONL (all on one line) into proper JSONL
(one JSON object per line).
"""

import json
import sys
from pathlib import Path

def fix_jsonl(input_file: Path, output_file: Path = None):
    """Fix JSONL file with all records on one line."""
    if output_file is None:
        output_file = input_file.with_suffix('.fixed.jsonl')
    
    print(f"Reading: {input_file}")
    
    # Read the single line
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # The file is a sequence of JSON objects concatenated: }{
    # We need to split on }{ and add back the braces
    
    # Split and reconstruct
    records = []
    depth = 0
    current = []
    
    for char in content:
        current.append(char)
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                # Complete JSON object
                obj_str = ''.join(current)
                try:
                    obj = json.loads(obj_str)
                    records.append(obj)
                    current = []
                except json.JSONDecodeError as e:
                    print(f"Error parsing object: {e}")
                    print(f"Content: {obj_str[:100]}...")
                    current = []
    
    print(f"Found {len(records)} records")
    
    # Write properly formatted JSONL
    print(f"Writing: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"✓ Done! {len(records)} records written")
    return len(records)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix JSONL files with all records on one line")
    parser.add_argument('input', type=Path, help="Input JSONL file")
    parser.add_argument('-o', '--output', type=Path, help="Output file (default: input.fixed.jsonl)")
    
    args = parser.parse_args()
    
    fix_jsonl(args.input, args.output)
