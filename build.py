import os
import sys

def build():
    # Read the clean, readable source file
    with open('src/widget.html', 'r', encoding='utf-8') as f:
        source_code = f.read()

    # Minify the code
    # Split by lines, strip leading/trailing spaces, and join into a single string
    lines = source_code.split('\n')
    minified = ''.join([line.strip() for line in lines])

    # Ensure dist folder exists
    os.makedirs('dist', exist_ok=True)

    # Write the minified version to dist/
    with open('dist/widget.min.html', 'w', encoding='utf-8') as f:
        f.write(minified)

    # Automatically update index.html preview page
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()

    start_marker = '<div id="space-countdown-widget"'
    end_marker = '</script></div>'

    start_idx = index_content.find(start_marker)
    # The end marker might vary slightly if the user edited it, so we find the closing div after the script
    end_idx = index_content.find('</div>', index_content.find('</script>')) + 6

    if start_idx != -1 and end_idx != -1:
        new_index = index_content[:start_idx] + minified + index_content[end_idx:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_index)
        print(f"Successfully minified src/widget.html -> dist/widget.min.html")
        print(f"Successfully updated index.html with new minified widget code!")
    else:
        print("Warning: Could not automatically inject into index.html (markers not found).")
        print("Your minified code is ready in dist/widget.min.html")

if __name__ == "__main__":
    build()
