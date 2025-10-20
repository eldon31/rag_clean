#!/usr/bin/env python3
"""Test tree-sitter-language-pack installation"""

from tree_sitter_language_pack import get_language

langs = ['python', 'javascript', 'typescript', 'java', 'go', 'rust', 'c', 'cpp']

print("Testing tree-sitter-language-pack...")
print("-" * 50)

for lang in langs:
    try:
        language = get_language(lang)
        print(f"✓ {lang:15} loaded successfully")
    except Exception as e:
        print(f"✗ {lang:15} failed: {e}")

print("-" * 50)
print(f"✓ All {len(langs)} languages tested!")