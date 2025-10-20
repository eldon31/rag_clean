#!/usr/bin/env python3
"""Quick test to verify Tree-sitter API fix"""

from tree_sitter import Parser
from tree_sitter_language_pack import get_language

# Test the new API
print("Testing Tree-sitter API fix...")
try:
    language = get_language("python")
    parser = Parser(language)  # New API: Pass language to constructor
    
    code = """
def hello():
    print("Hello, World!")
"""
    
    tree = parser.parse(code.encode('utf-8'))
    print(f"✓ Tree-sitter works! Root node type: {tree.root_node.type}")
    print(f"✓ Code has {len(tree.root_node.children)} top-level nodes")
    
except Exception as e:
    print(f"✗ Tree-sitter failed: {e}")