# Space Flight Widget

An embeddable, responsive countdown widget designed specifically for forums and websites. It automatically fetches the next upcoming heavy-lift rocket launch (Starship, Falcon Heavy, Ariane 6, etc.) using [The Space Devs API](https://thespacedevs.com/).

## Features
- **Dutch Localization**: Fully translated interface and launch statuses.
- **BBCode Compatible**: Built entirely with inline styles and ES5 Javascript to bypass strict forum sanitizers and `[html]` tags.
- **Smart Logic**: Automatically displays a fallback message if there isn't a heavy-lift launch scheduled within the next 7 days.
- **Zero Dependencies**: Pure HTML and JavaScript. No external CSS stylesheets or libraries required.

## How to Edit
The widget code is minified to a single line to bypass strict forum BBCode sanitizers (which often break scripts by converting newlines into `<br>` tags). To edit the widget:
1. Make your changes in the clean, human-readable `src/widget.html` file.
2. Run the build script to compile and minify your code:
   ```bash
   python3 build.py
   ```
3. The script will generate a single-line minified version in `dist/widget.min.html` and automatically update the `index.html` preview.

## How to Embed
Simply copy the raw, single-line code from `dist/widget.min.html` and paste it into your website or forum's HTML embed block (e.g., using `[html]...[/html]`).

## Attribution
Launch data is provided by [The Space Devs](https://thespacedevs.com/).

## License
MIT License. See `LICENSE` for more information.
