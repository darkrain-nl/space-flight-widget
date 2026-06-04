import os
import re

def validate_script(script, i):
    # 1. Check for single-line comments // (excluding http:// and https://)
    if re.search(r'(?<!https:)(?<!http:)\/\/', script):
        raise ValueError(
            "Error: Found single-line JS comment '//' in script tag. "
            "This will break minification onto a single line! Please use '/* ... */' instead."
        )
    
    # 2. Check for mismatched curly braces
    open_braces = script.count('{')
    close_braces = script.count('}')
    if open_braces != close_braces:
        raise ValueError(
            f"Error: Mismatched curly braces in JavaScript block #{i} "
            f"({open_braces} open, {close_braces} close)."
        )
    
    # 3. Check for mismatched parentheses
    open_parens = script.count('(')
    close_parens = script.count(')')
    if open_parens != close_parens:
        raise ValueError(
            f"Error: Mismatched parentheses in JavaScript block #{i} "
            f"({open_parens} open, {close_parens} close)."
        )

    # 4. Check for smiley bug sequences
    if '})' in script:
        raise ValueError(
            f"Error: Found smiley-triggering sequence '}})' in JavaScript block #{i}. "
            "This will break in some forum BBCode parsers. Please write '} )' with a space instead."
        )
    if '8)' in script:
        raise ValueError(
            f"Error: Found smiley-triggering sequence '8)' in JavaScript block #{i}. "
            "This will break in some forum BBCode parsers (converting to cool glasses emoji). "
            "Please write '8 )' or '7 + 1' instead."
        )

def minify_code(source_code):
    # Syntax and comment validation checks on Javascript blocks
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script\b[^>]*>', source_code, flags=re.DOTALL | re.IGNORECASE)
    for i, script in enumerate(scripts, 1):
        validate_script(script, i)

    # Strip block comments /* ... */ to save bytes in the minified version
    minified_src = re.sub(r'/\*.*?\*/', '', source_code, flags=re.DOTALL)

    # Minify the code
    # Split by lines, strip leading/trailing spaces, and join into a single string
    lines = minified_src.split('\n')
    return ''.join([line.strip() for line in lines])

def build():
    # Read the clean, readable source file
    with open('src/widget.html', 'r', encoding='utf-8') as f:
        source_code = f.read()

    minified = minify_code(source_code)

    # Ensure dist folder exists
    os.makedirs('dist', exist_ok=True)

    # Write the minified version to dist/
    with open('dist/widget.min.html', 'w', encoding='utf-8') as f:
        f.write(minified)

    # Automatically update index.html preview page
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()

    start_marker = '<div id="space-countdown-widget"'

    start_idx = index_content.find(start_marker)
    # The end marker might vary slightly if the user edited it, so we find the closing div after the script
    end_idx = index_content.find('</div>', index_content.find('</script>')) + 6

    if start_idx != -1 and end_idx != -1:
        new_index = index_content[:start_idx] + minified + index_content[end_idx:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_index)
        print("Successfully minified src/widget.html -> dist/widget.min.html")
        print("Successfully updated index.html with new minified widget code!")
    else:
        print("Warning: Could not automatically inject into index.html (markers not found).")
        print("Your minified code is ready in dist/widget.min.html")

if __name__ == "__main__":
    build()
