#!/usr/bin/env python3
"""
Simple verification script to check bot structure without requiring dependencies.
"""

import ast
import sys

def verify_bot_structure(filename):
    """Verify the bot Python file has valid structure."""
    print(f"Verifying {filename}...")
    
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        # Parse the AST
        tree = ast.parse(code)
        
        # Check for required components
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        print(f"✓ Valid Python syntax")
        print(f"✓ Found {len(classes)} class(es): {', '.join(classes)}")
        print(f"✓ Found {len(functions)} function(s)")
        
        # Check for main class
        if 'PokemonCenterBot' in classes:
            print("✓ PokemonCenterBot class found")
        else:
            print("✗ PokemonCenterBot class not found")
            return False
        
        # Check for key methods
        required_methods = ['check_product_availability', 'attempt_checkout', 'monitor_and_purchase']
        for method in required_methods:
            if method in functions:
                print(f"✓ Method '{method}' found")
            else:
                print(f"✗ Method '{method}' not found")
                return False
        
        print("\n✓ All checks passed!")
        return True
        
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    success = verify_bot_structure('pokemon_bot.py')
    sys.exit(0 if success else 1)
