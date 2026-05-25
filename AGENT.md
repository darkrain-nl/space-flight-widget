# Agent Instructions

Hello fellow AI! If you are tasked with modifying this repository, please read and follow these rules strictly to ensure you do not break the widget's compatibility with forum BBCode parsers.

## Workflow Rules
1. **Never edit `index.html` or `dist/widget.min.html` directly.** Those files are automatically generated.
2. **Edit Source Only**: Make all of your code changes (HTML, CSS, JavaScript) inside `src/widget.html`.
3. **Build the Project**: After modifying `src/widget.html`, you MUST run the build script:
   ```bash
   python3 build.py
   ```
   This script will minify the code and inject it into the correct distribution files.
4. **Pull Requests Required**: Direct pushes to `main` are blocked by repository rules. You must commit your changes to a new branch, push the branch, and use the `gh` CLI to create a pull request if it is available.

## Crucial Technical Constraints
This widget is designed to be copy-pasted into restrictive forum software using an `[html]...[/html]` BBCode tag.

- **Strict Single-Line Output**: The forum parser automatically injects `<br>` tags for every newline character (`\n`). If there are any newlines inside the `<script>` tags, the injected `<br>` will cause a syntax error (`expected expression, got '<'`) and break the widget. The build script (`build.py`) handles removing newlines, so do not alter its minification logic.
- **The Smiley Bug (`})`)**: Some forum BBCode parsers will automatically convert the exact sequence `})` into a smiley face image (`<img src="...">`). This breaks JavaScript syntax. When writing JavaScript in `src/widget.html`, you **must** leave a space between closing brackets, like this: `} )`. Do not ever write `})`.
- **Inline Styles Only**: The forum strips out `<style>...</style>` blocks. All CSS must be written as inline `style="..."` attributes on the HTML elements themselves.
- **ES5 JavaScript**: To maximize compatibility with strict sanitizers, the JavaScript is written using older ES5 syntax (`var`, `function()`). Avoid modern features like `let`, `const`, arrow functions (`=>`), and optional chaining (`?.`). Avoid `//` comments as they will comment out the rest of the script when minified onto a single line.

## Lessons Learned
- **Content-Security-Policy (CSP) for External Images**: If you are embedding images from external sources (e.g. The Space Devs CDN: `https://thespacedevs-prod.nyc3.digitaloceanspaces.com`), ensure that `img-src` in `index.html`'s `<meta http-equiv="Content-Security-Policy">` allows that domain to prevent images from being blocked in the preview.
- **Handling API Rate Limits (HTTP 429)**: The Space Devs public API limits unauthenticated requests to 15 per hour per IP. It returns a 429 status code when exceeded, containing a `detail` message with the throttle duration (e.g. `{"detail":"Request was throttled. Expected available in 625 seconds."}`). The widget dynamically parses this timeout string and schedules the next fetch attempt after the throttle clears, preventing infinite loops that hammer the server.
- **GitHub Image Caching**: GitHub aggressively caches images via its Camo proxy. When replacing an image like `assets/preview.gif`, update the `<img>` tag in `README.md` to append a cache-busting query parameter (e.g. `?v=2`) to force GitHub to serve the updated image immediately.
