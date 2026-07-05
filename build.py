import os
import re

SCRIPT_TAG_RE = re.compile(
    r"<script\b[^>]*>(.*?)</script\b[^>]*>", re.DOTALL | re.IGNORECASE
)

PLAIN_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)

# Characters after which a '/' starts a regex literal rather than division
# (standard heuristic; a '/' after a value would be division)
_REGEX_PRECEDING_CHARS = "([{=,:;!&|?+-*%~^<>"


def extract_scripts(source_code):
    """Return the contents of every <script> block in the given HTML."""
    return SCRIPT_TAG_RE.findall(source_code)


def _scan_js(script, remove_line_comments, blank_strings):
    """Single-pass JavaScript scanner used for comment stripping and static
    analysis. Removes /* ... */ comments without ever touching the inside of
    string or regex literals; optionally removes // comments (string-aware,
    so URLs are safe) and blanks string literal contents (so patterns inside
    strings cannot mask or fake violations in the quality checks)."""
    out = []
    i = 0
    n = len(script)
    last_code = ""  # last non-whitespace character emitted
    while i < n:
        c = script[i]
        nxt = script[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "*":
            end = script.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue
        if remove_line_comments and c == "/" and nxt == "/":
            end = script.find("\n", i + 2)
            i = n if end == -1 else end
            continue
        if c in ("'", '"'):
            quote = c
            out.append(c)
            i += 1
            while i < n:
                s = script[i]
                if s == "\\":
                    if not blank_strings:
                        out.append(script[i : i + 2])
                    i += 2
                    continue
                if s == quote:
                    out.append(s)
                    i += 1
                    break
                if not blank_strings:
                    out.append(s)
                i += 1
            last_code = quote
            continue
        if c == "/" and (last_code == "" or last_code in _REGEX_PRECEDING_CHARS):
            # Regex literal: copy verbatim up to the unescaped closing '/',
            # so quotes or comment markers inside it cannot derail the scan
            start = i
            i += 1
            in_class = False
            while i < n:
                r = script[i]
                if r == "\\":
                    i += 2
                    continue
                if r == "[":
                    in_class = True
                elif r == "]":
                    in_class = False
                elif r == "/" and not in_class:
                    i += 1
                    break
                elif r == "\n":
                    break
                i += 1
            out.append(script[start:i])
            last_code = "/"
            continue
        out.append(c)
        if not c.isspace():
            last_code = c
        i += 1
    return "".join(out)


def strip_js_block_comments(script):
    """Remove /* ... */ comments from JavaScript without corrupting string
    or regex literals that contain comment markers."""
    return _scan_js(script, remove_line_comments=False, blank_strings=False)


def clean_js_for_analysis(script):
    """Prepare JavaScript for static checks: remove all comments and blank
    out string literal contents."""
    return _scan_js(script, remove_line_comments=True, blank_strings=True)


def strip_block_comments(source_code):
    """Strip /* ... */ comments from an HTML document: string/regex-aware
    inside <script> blocks, plain regex elsewhere (HTML and inline CSS
    contain no string literals that need protecting)."""
    result = []
    last = 0
    for m in SCRIPT_TAG_RE.finditer(source_code):
        result.append(PLAIN_BLOCK_COMMENT_RE.sub("", source_code[last : m.start(1)]))
        result.append(strip_js_block_comments(m.group(1)))
        last = m.end(1)
    result.append(PLAIN_BLOCK_COMMENT_RE.sub("", source_code[last:]))
    return "".join(result)


def validate_script(script, i):
    # 1. Check for single-line comments // (excluding http:// and https://)
    if re.search(r"(?<!https:)(?<!http:)\/\/", script):
        raise ValueError(
            "Error: Found single-line JS comment '//' in script tag. "
            "This will break minification onto a single line! Please use '/* ... */' instead."
        )

    # 2. Check for mismatched curly braces
    open_braces = script.count("{")
    close_braces = script.count("}")
    if open_braces != close_braces:
        raise ValueError(
            f"Error: Mismatched curly braces in JavaScript block #{i} "
            f"({open_braces} open, {close_braces} close)."
        )

    # 3. Check for mismatched parentheses
    open_parens = script.count("(")
    close_parens = script.count(")")
    if open_parens != close_parens:
        raise ValueError(
            f"Error: Mismatched parentheses in JavaScript block #{i} "
            f"({open_parens} open, {close_parens} close)."
        )

    # 4. Check for smiley bug sequences
    if "})" in script:
        raise ValueError(
            f"Error: Found smiley-triggering sequence '}})' in JavaScript block #{i}. "
            "This will break in some forum BBCode parsers. Please write '} )' with a space instead."
        )
    if "8)" in script:
        raise ValueError(
            f"Error: Found smiley-triggering sequence '8)' in JavaScript block #{i}. "
            "This will break in some forum BBCode parsers (converting to cool glasses emoji). "
            "Please write '8 )' or '7 + 1' instead."
        )

    # 5. Check for line endings that automatic semicolon insertion would
    # reinterpret when the build joins all lines into one: a bare
    # 'return'/'break'/'continue'/'throw' silently captures the next line's
    # expression, and a trailing ++/-- attaches to the next line.
    for lineno, raw_line in enumerate(script.split("\n"), 1):
        line = raw_line.strip()
        if (
            re.search(r"\b(?:return|break|continue|throw)$", line)
            or line.endswith("++")
            or line.endswith("--")
        ):
            raise ValueError(
                f"Error: Line {lineno} of JavaScript block #{i} ends in a token "
                f"that changes meaning when minified onto a single line: {line!r}. "
                "Keep the statement on one line."
            )


def minify_code(source_code):
    # Syntax and comment validation checks on Javascript blocks
    for i, script in enumerate(extract_scripts(source_code), 1):
        validate_script(script, i)

    # Strip block comments /* ... */ to save bytes in the minified version
    # (string/regex-aware inside scripts so literals are never corrupted)
    minified_src = strip_block_comments(source_code)

    # Minify the code
    # Split by lines, strip leading/trailing spaces, and join into a single string
    lines = minified_src.split("\n")
    minified = "".join([line.strip() for line in lines])

    # Re-validate the final output: joining lines can itself create smiley
    # sequences or unbalanced blocks that the source-level checks cannot see
    for i, script in enumerate(extract_scripts(minified), 1):
        validate_script(script, i)

    return minified


def build():
    # Read the clean, readable source file
    with open("src/widget.html", "r", encoding="utf-8") as f:
        source_code = f.read()

    minified = minify_code(source_code)

    # Ensure dist folder exists
    os.makedirs("dist", exist_ok=True)

    # Write the minified version to dist/
    with open("dist/widget.min.html", "w", encoding="utf-8") as f:
        f.write(minified)

    # Automatically update index.html preview page
    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()

    start_marker = '<div id="space-countdown-widget"'

    # Anchor every search to the previous match so the splice region cannot
    # accidentally resolve to an unrelated </script> or </div> elsewhere in
    # the file (e.g. if a script tag is ever added above the widget block).
    start_idx = index_content.find(start_marker)
    end_idx = -1
    if start_idx != -1:
        script_close_idx = index_content.find("</script>", start_idx)
        if script_close_idx != -1:
            div_close_idx = index_content.find("</div>", script_close_idx)
            if div_close_idx != -1:
                end_idx = div_close_idx + len("</div>")

    if start_idx != -1 and end_idx != -1:
        new_index = index_content[:start_idx] + minified + index_content[end_idx:]
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_index)
        print("Successfully minified src/widget.html -> dist/widget.min.html")
        print("Successfully updated index.html with new minified widget code!")
    else:
        print("Error: Could not inject into index.html (widget markers not found).")
        print("Your minified code is ready in dist/widget.min.html")
        raise SystemExit(1)


if __name__ == "__main__":
    build()
