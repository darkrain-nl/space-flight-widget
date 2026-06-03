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
5. **Local Verification**: Do not open `index.html` as a local `file://` URI in the browser because the browser's sandbox/CSP may block API requests. Instead, spin up a local web server (e.g., `python3 -m http.server 8090`) and navigate to `http://localhost:8090/index.html` to test.


## Crucial Technical Constraints
This widget is designed to be copy-pasted into restrictive forum software using an `[html]...[/html]` BBCode tag.

- **Strict Single-Line Output**: The forum parser automatically injects `<br>` tags for every newline character (`\n`). If there are any newlines inside the `<script>` tags, the injected `<br>` will cause a syntax error (`expected expression, got '<'`) and break the widget. The build script (`build.py`) handles removing newlines, so do not alter its minification logic.
- **The Smiley Bug (`})`)**: Some forum BBCode parsers will automatically convert the exact sequence `})` into a smiley face image (`<img src="...">`). This breaks JavaScript syntax. When writing JavaScript in `src/widget.html`, you **must** leave a space between closing brackets, like this: `} )`. Do not ever write `})`.
- **Inline Styles Only**: The forum strips out `<style>...</style>` blocks. All CSS must be written as inline `style="..."` attributes on the HTML elements themselves.
- **ES5 JavaScript**: To maximize compatibility with strict sanitizers, the JavaScript is written using older ES5 syntax (`var`, `function()`). Avoid modern features like `let`, `const`, arrow functions (`=>`), and optional chaining (`?.`). Avoid `//` comments as they will comment out the rest of the script when minified onto a single line.

## Lessons Learned
- **Content-Security-Policy (CSP) for External Images**: If you are embedding images from external sources (e.g. The Space Devs CDN: `https://thespacedevs-prod.nyc3.digitaloceanspaces.com`), ensure that `img-src` in `index.html`'s `<meta http-equiv="Content-Security-Policy">` allows that domain to prevent images from being blocked in the preview.
- **Handling API Rate Limits and Smart Caching**: The Space Devs public API limits unauthenticated requests to 15 per hour per IP. To prevent hitting the limit:
  1. The widget uses a cache-first approach, serving from `localStorage` immediately on load and fetching in the background if the cache is stale.
  2. The refresh interval is dynamic based on launch proximity (ranging from 5 minutes when <1 hour from launch up to 30 minutes when days away/no launch).
  3. Stored quota status is monitored by fetching the `/api-throttle` endpoint after every successful launch data fetch (since it is free and does not count against rate limits).
  4. If near the rate limit (`current_use >= limit - 3`), it skips the data fetch, falls back to cache, and retries once the throttle window resets (`next_use_secs`).
  5. If a 429 status is still hit, it parses the throttle duration string (e.g., `{"detail":"Request was throttled. Expected available in 625 seconds."}`) to schedule the next fetch.
- **GitHub Image Caching**: GitHub aggressively caches images via its Camo proxy. When replacing an image like `assets/preview.gif`, update the `<img>` tag in `README.md` to append a cache-busting query parameter (e.g. `?v=2`) to force GitHub to serve the updated image immediately.
- **Strict Frontend Security (XSS & UX)**: When writing any HTML or JavaScript for this project (including the `index.html` preview page), you must strictly adhere to secure web standards. Never use dangerous DOM sinks like `innerHTML` (use `DOMParser` or standard DOM elements instead) to prevent XSS. Additionally, never use blocking native dialogues like `alert()`, `confirm()`, or `prompt()`—use non-blocking UI components (like custom toast notifications) instead.
