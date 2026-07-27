/* Shared widget loader used by index.html (preview page) and embed.html
   (iframe embeds). Owns the fetch/configure/mount pipeline so both pages
   behave identically - edit here, never copy into the pages. */
(function() {
    'use strict';

    function escapeAttr(value) {
        return String(value === undefined || value === null ? '' : value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    /* Fetch the minified widget template with error propagation. */
    function fetchWidgetTemplate(url) {
        return fetch(url).then(function(res) {
            if (!res.ok) {
                throw new Error('Failed to load widget template (HTTP ' + res.status + ')');
            }
            return res.text();
        });
    }

    /* Inject the configuration attributes into the widget template string.
       The result is the embed-ready HTML - exactly what preview users copy. */
    function buildWidgetHtml(template, options) {
        var attrs = 'data-lang="' + escapeAttr(options.lang || 'en') + '"';
        if (options.rockets) {
            attrs += ' data-rockets="' + escapeAttr(options.rockets) + '"';
        }
        attrs += ' data-days="' + escapeAttr(options.days || 7) + '"';
        /* Function replacement, not a string: a literal replacement would let a
           '$&' or "$'" in an option value expand to surrounding template markup
           and splice a second copy of the widget into the opening tag. */
        return template.replace('data-lang="en"', function() { return attrs; });
    }

    /* Parse the widget HTML via DOMParser (avoiding innerHTML), apply the
       visual options, mount into container and re-execute the widget's
       script blocks (parser-inserted scripts are inert by spec). */
    function mountWidget(container, html, options) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        var widget = doc.querySelector('#space-countdown-widget');
        if (widget) {
            if (options.bg === 'transparent') {
                widget.style.background = 'transparent';
                widget.style.backgroundColor = 'transparent';
                widget.style.border = 'none';
                widget.style.boxShadow = 'none';
            } else if (options.bg) {
                widget.style.background = options.bg;
            }
            if (options.hideAttr) {
                var attr = doc.getElementById('space-attribution');
                if (attr) {
                    attr.style.display = 'none';
                }
            }
            if (options.lightTheme) {
                widget.classList.add('light-theme');
            }
        }
        container.replaceChildren();
        while (doc.body.firstChild) {
            container.appendChild(doc.body.firstChild);
        }
        var scripts = container.getElementsByTagName('script');
        for (var i = 0; i < scripts.length; i++) {
            var newScript = document.createElement('script');
            newScript.text = scripts[i].text;
            document.body.appendChild(newScript).parentNode.removeChild(newScript);
        }
    }

    window.SpaceWidgetLoader = {
        fetchWidgetTemplate: fetchWidgetTemplate,
        buildWidgetHtml: buildWidgetHtml,
        mountWidget: mountWidget
    };
})();
