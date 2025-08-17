#!/usr/bin/env python3
"""
Fix unicode characters in enhanced_crypto_backtest.py for subprocess compatibility
"""

import re

def fix_unicode_in_file(filepath):
    """Remove unicode characters from file"""
    unicode_replacements = {
        '🚀': '',
        '📊': '',
        '💰': '',
        '🔥': '',
        '🎯': '',
        '⚡️': '',
        '📈': '',
        '💹': '',
        '📉': '',
        '🎉': '',
        '❌': '',
        '⚠️': 'WARNING:',
        '✅': '',
        '💀': '',
        '🤖': '',
        '🧪': '',
        '⏰': '',
        '🏢': '',
        '📁': '',
        '📝': '',
        '🌟': '',
    }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace unicode characters
    for unicode_char, replacement in unicode_replacements.items():
        content = content.replace(unicode_char, replacement)
    
    # Clean up extra spaces
    content = re.sub(r' +', ' ', content)
    content = re.sub(r'^ +', '', content, flags=re.MULTILINE)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed unicode characters in {filepath}")
        return True
    else:
        print(f"No changes needed in {filepath}")
        return False

if __name__ == "__main__":
    fix_unicode_in_file("enhanced_crypto_backtest.py")
