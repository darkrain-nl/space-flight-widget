# Contributing to Space Flight Widget

Thank you for your interest in contributing! This widget is designed to be highly compatible with restrictive forum software (specifically BBCode `[html]` tags). Because of this, we have some unusual but **critical technical constraints** you must follow.

## Workflow

1. **Edit Source Only**: Make all of your code changes (HTML, CSS, JavaScript) inside `src/widget.html`.
2. **Never edit `index.html` or `dist/widget.min.html` directly.** Those files are automatically generated.
3. **Build the Project**: After modifying `src/widget.html`, you MUST run the build script:
   ```bash
   python3 build.py
   ```
4. **Preview**: Open `index.html` in your browser to verify your changes look good.
5. **Commit**: Commit your changes and open a Pull Request.

## Critical Technical Constraints

If you don't follow these rules, the widget will break when pasted into a forum.

### 1. Strict Single-Line Output
Forum parsers automatically inject `<br>` tags for every newline character (`\n`). If there are any newlines inside the `<script>` tags, the injected `<br>` will cause a syntax error (`expected expression, got '<'`) and break the widget. 
* **Rule**: The build script (`build.py`) handles removing newlines. Do not alter its minification logic.

### 2. The Smiley Bug (`})`)
Some forum BBCode parsers will automatically convert the exact sequence `})` into a smiley face image (`<img src="...">`). This completely breaks JavaScript syntax.
* **Rule**: When writing JavaScript in `src/widget.html`, you **must** leave a space between closing brackets, like this: `} )`. Do not ever write `})`.

### 3. Inline Styles Only
Many forums strip out `<style>...</style>` blocks for security reasons.
* **Rule**: All CSS must be written as inline `style="..."` attributes on the HTML elements themselves.

### 4. ES5 JavaScript Only
To maximize compatibility with older browsers and strict HTML sanitizers, we avoid modern JS features.
* **Rule**: Use older ES5 syntax (`var`, `function()`). Avoid modern features like `let`, `const`, arrow functions (`=>`), and optional chaining (`?.`).
* **Rule**: Avoid `//` comments in your JavaScript. When the build script minifies the code onto a single line, a `//` comment will accidentally comment out the rest of the entire script!

## Security
If you are modifying how data is injected into the DOM, **always use `.textContent`** instead of `.innerHTML` for any data sourced from the API to prevent XSS vulnerabilities.

Thank you for helping us keep this widget awesome and functional! 🚀
