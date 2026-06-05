import unittest
import os
import re

# Base directory setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestWidgetQualityAndConstraints(unittest.TestCase):
    def read_file_content(self, relative_path):
        path = os.path.join(BASE_DIR, relative_path)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def get_javascript_blocks(self, html_content):
        # Extracts everything inside <script>...</script> tags
        return re.findall(
            r"<script\b[^>]*>(.*?)</script\b[^>]*>",
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )

    def clean_js(self, js_content):
        # Remove block comments /* ... */
        js_content = re.sub(r"/\*.*?\*/", "", js_content, flags=re.DOTALL)
        # Remove single line comments // ... (excluding URL protocols)
        js_content = re.sub(r"(?<!https:)(?<!http:)\/\/.*", "", js_content)
        # Remove double-quoted strings
        js_content = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', "", js_content)
        # Remove single-quoted strings
        js_content = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "", js_content)
        return js_content

    def test_es5_conformance(self):
        """Verify that the JavaScript code uses only ES5 syntax and doesn't contain ES6+ features."""
        source_code = self.read_file_content("src/widget.html")
        js_blocks = self.get_javascript_blocks(source_code)

        for i, js in enumerate(js_blocks, 1):
            clean = self.clean_js(js)

            # 1. Check for 'const' and 'let' with word boundaries
            if re.search(r"\bconst\b", clean):
                self.fail(
                    f"JavaScript block #{i} in src/widget.html contains ES6 'const' keyword! Please use 'var' instead."
                )
            if re.search(r"\blet\b", clean):
                self.fail(
                    f"JavaScript block #{i} in src/widget.html contains ES6 'let' keyword! Please use 'var' instead."
                )

            # 2. Check for arrow functions '=>'
            if "=>" in clean:
                self.fail(
                    f"JavaScript block #{i} in src/widget.html contains ES6 arrow function '=>'! Please use standard ES5 'function()' syntax."
                )

            # 3. Check for template literals (backticks)
            if "`" in clean:
                self.fail(
                    f"JavaScript block #{i} in src/widget.html contains ES6 template literals (backticks)! Please use single or double quotes."
                )

            # 4. Check for optional chaining '?.'
            # Check for ?. but be careful not to match standard ternary expressions like `x ? 1 : 2` or float numbers like `.5`.
            # A ?. sequence is '?.' not followed by a digit.
            if re.search(r"\?\.(?!\d)", clean):
                self.fail(
                    f"JavaScript block #{i} in src/widget.html contains ES2020 optional chaining '?.'! Please use standard conditional checks."
                )

            # 5. Check for ES6 class declaration
            if re.search(r"\bclass\b", clean):
                self.fail(
                    f"JavaScript block #{i} in src/widget.html contains ES6 'class' keyword! Please use prototype-based objects."
                )

            # 6. Check for Rest/Spread operator
            # A spread operator is three dots followed by a variable/expression name, e.g. ...x
            # Let's check for '...' outside strings and comments.
            if "..." in clean:
                self.fail(
                    f"JavaScript block #{i} in src/widget.html contains ES6 spread/rest operator '...'!"
                )

    def test_no_style_tags(self):
        """Verify that src/widget.html does not contain any <style> tags."""
        source_code = self.read_file_content("src/widget.html")
        self.assertNotIn(
            "<style",
            source_code.lower(),
            "src/widget.html must not contain '<style>' tags. All styles must be inline.",
        )
        self.assertNotIn(
            "</style>",
            source_code.lower(),
            "src/widget.html must not contain '</style>' tags. All styles must be inline.",
        )

    def test_no_unsafe_dom_sinks(self):
        """Verify that no file uses unsafe DOM sinks (assignment to innerHTML/outerHTML, or document.write, insertAdjacentHTML) or blocking native dialogues (alert, confirm, prompt)."""
        files_to_check = ["src/widget.html", "embed.html", "index.html"]

        for rel_path in files_to_check:
            content = self.read_file_content(rel_path)
            js_blocks = self.get_javascript_blocks(content)

            for i, js in enumerate(js_blocks, 1):
                clean = self.clean_js(js)

                # Check unsafe sinks (assignments to innerHTML/outerHTML or calls to write/insertAdjacentHTML)
                if re.search(r'\.innerHTML\s*=|\[[\'"]innerHTML[\'"]\]\s*=', clean):
                    self.fail(
                        f"JavaScript block #{i} in {rel_path} assigns to dangerous DOM sink 'innerHTML'! Use textContent, DOMParser, or replaceChildren instead to prevent XSS."
                    )
                if re.search(r'\.outerHTML\s*=|\[[\'"]outerHTML[\'"]\]\s*=', clean):
                    self.fail(
                        f"JavaScript block #{i} in {rel_path} assigns to dangerous DOM sink 'outerHTML'! Use safe elements builder APIs instead to prevent XSS."
                    )
                if "document.write" in clean:
                    self.fail(
                        f"JavaScript block #{i} in {rel_path} calls 'document.write'! This is a dangerous DOM sink."
                    )
                if "insertAdjacentHTML" in clean:
                    self.fail(
                        f"JavaScript block #{i} in {rel_path} calls 'insertAdjacentHTML'! Use textContent or DOMParser instead."
                    )

                # Check native blocking dialogues
                for dialogue in ["alert", "confirm", "prompt"]:
                    # Use word boundary to avoid variables like 'alerts'
                    if re.search(r"\b" + dialogue + r"\b", clean):
                        self.fail(
                            f"JavaScript block #{i} in {rel_path} uses blocking dialogue '{dialogue}'! Use non-blocking custom UI notification components instead."
                        )

    def test_i18n_translation_keys(self):
        """Verify that all language translations in the i18n object have the exact same keys as the English (en) dictionary."""
        source_code = self.read_file_content("src/widget.html")

        # Locate the i18n block
        i18n_match = re.search(r"var\s+i18n\s*=\s*\{([\s\S]*?)\};", source_code)
        self.assertIsNotNone(
            i18n_match, "Could not find i18n object definition in src/widget.html"
        )
        i18n_content = i18n_match.group(1)

        # Find all languages inside i18n (e.g. en: { ... })
        lang_blocks = re.findall(r"(\w+)\s*:\s*\{([^}]+)\}", i18n_content)
        self.assertTrue(
            len(lang_blocks) > 0, "No language blocks found in i18n definition"
        )

        # Build dictionary of language -> set of keys
        lang_keys = {}
        for lang, block in lang_blocks:
            cleaned_block = self.clean_js(block)
            # Find all keys (words followed by a colon)
            keys = re.findall(r"(\w+)\s*:", cleaned_block)
            lang_keys[lang] = set(keys)

        self.assertIn(
            "en", lang_keys, "English (en) translation is missing from i18n dictionary"
        )
        en_keys = lang_keys["en"]

        # Compare all other languages with English keys
        for lang, keys in lang_keys.items():
            if lang == "en":
                continue

            missing_keys = en_keys - keys
            extra_keys = keys - en_keys

            self.assertEqual(
                len(missing_keys),
                0,
                f"Language '{lang}' is missing translation keys: {missing_keys}",
            )
            self.assertEqual(
                len(extra_keys),
                0,
                f"Language '{lang}' has extra translation keys: {extra_keys}",
            )

    def test_widget_size_budget(self):
        """Verify that the compiled widget.min.html size is within the 64KB budget for forum post limits."""
        minified_path = os.path.join(BASE_DIR, "dist", "widget.min.html")
        if not os.path.exists(minified_path):
            self.skipTest(
                "dist/widget.min.html does not exist yet. Please run build.py first."
            )

        size = os.path.getsize(minified_path)
        # Limit to 64KB (65536 bytes)
        self.assertLess(
            size,
            65536,
            f"Minified widget size ({size} bytes) exceeds the budget of 64KB!",
        )

    def test_smiley_and_comment_regression_on_dist(self):
        """Verify that dist/widget.min.html has no smiley triggers or single-line comments in script tags."""
        minified_path = os.path.join(BASE_DIR, "dist", "widget.min.html")
        if not os.path.exists(minified_path):
            self.skipTest(
                "dist/widget.min.html does not exist yet. Please run build.py first."
            )

        with open(minified_path, "r", encoding="utf-8") as f:
            minified_code = f.read()

        # Verify no single-line JS comments (excluding urls)
        js_blocks = self.get_javascript_blocks(minified_code)
        for i, js in enumerate(js_blocks, 1):
            if re.search(r"(?<!https:)(?<!http:)\/\/", js):
                self.fail(
                    f"Found single-line JS comment '//' in dist/widget.min.html script block #{i}!"
                )

            # Verify no smiley triggers
            self.assertNotIn(
                "})",
                js,
                f"Found smiley trigger '}})' in dist/widget.min.html script block #{i}!",
            )
            self.assertNotIn(
                "8)",
                js,
                f"Found smiley trigger '8)' in dist/widget.min.html script block #{i}!",
            )

    def test_widget_version_consistency(self):
        """Verify that the widget's HTML data-version attribute matches the JS WIDGET_VERSION constant, and conforms to Semantic Versioning."""
        source_code = self.read_file_content("src/widget.html")

        # 1. Extract data-version from HTML root div
        html_version_match = re.search(
            r'\bdata-version=["\']([^"\']+)["\']', source_code
        )
        self.assertIsNotNone(
            html_version_match,
            "Could not find 'data-version' attribute in src/widget.html root div",
        )
        html_version = html_version_match.group(1)

        # 2. Extract WIDGET_VERSION from JS
        js_version_match = re.search(
            r'\bWIDGET_VERSION\s*=\s*["\']([^"\']+)["\']', source_code
        )
        self.assertIsNotNone(
            js_version_match,
            "Could not find 'WIDGET_VERSION' variable definition in src/widget.html script tag",
        )
        js_version = js_version_match.group(1)

        # 3. Assert matching and correct SemVer format
        self.assertEqual(
            html_version,
            js_version,
            f"Version mismatch! HTML data-version is '{html_version}', but JS WIDGET_VERSION is '{js_version}'.",
        )

        semver_pattern = r"^\d+\.\d+\.\d+$"
        self.assertTrue(
            re.match(semver_pattern, html_version),
            f"Version '{html_version}' does not conform to Semantic Versioning (X.Y.Z).",
        )


if __name__ == "__main__":
    unittest.main()
