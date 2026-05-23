# Space Flight Widget

An embeddable, responsive countdown widget designed specifically for forums and websites. It automatically fetches the next upcoming heavy-lift rocket launch (Starship, Falcon Heavy, Ariane 6, etc.) using [The Space Devs API](https://thespacedevs.com/).

## Features
- **Dutch Localization**: Fully translated interface and launch statuses.
- **BBCode Compatible**: Built entirely with inline styles and ES5 Javascript to bypass strict forum sanitizers and `[html]` tags (like on Tweakers.net).
- **Smart Logic**: Automatically displays a fallback message if there isn't a heavy-lift launch scheduled within the next 7 days.
- **Zero Dependencies**: Pure HTML and JavaScript. No external CSS stylesheets or libraries required.

## Usage
Simply copy the raw code block inside `index.html` (the `<div id="space-countdown-widget"...` block) and paste it into your website or forum's HTML embed block.

## Attribution
Launch data is provided by [The Space Devs](https://thespacedevs.com/).

## License
MIT License. See `LICENSE` for more information.
