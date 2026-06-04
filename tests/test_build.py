import unittest
import sys
import os

# Add parent directory to path so we can import build
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from build import minify_code

class TestBuildMinifier(unittest.TestCase):
    def test_successful_minification(self):
        sample_code = """
        <div>
            /* Sample block comment */
            <script>
                (function() {
                    var x = 5; /* inline block comment */
                    var y = 10;
                } )();
            </script>
        </div>
        """
        minified = minify_code(sample_code)
        self.assertNotIn("/*", minified)
        self.assertNotIn("*/", minified)
        self.assertIn("var x = 5;var y = 10;", minified)
        # Check that whitespace is minified
        self.assertNotIn("\n", minified)

    def test_single_line_comment_throws(self):
        sample_code = """
        <script>
            var x = 5; // This is a single line comment that should throw
        </script>
        """
        with self.assertRaises(ValueError) as ctx:
            minify_code(sample_code)
        self.assertIn("single-line JS comment", str(ctx.exception))

    def test_script_attributes_and_case_validation(self):
        # Test that mixed case and attributes are matched and validated
        sample_code = """
        <SCRIPT type="text/javascript">
            var x = 5; // This single line comment should throw even in uppercase/attr tags
        </SCRIPT>
        """
        with self.assertRaises(ValueError) as ctx:
            minify_code(sample_code)
        self.assertIn("single-line JS comment", str(ctx.exception))

    def test_url_slashes_do_not_throw(self):
        sample_code = """
        <script>
            var url = 'https://example.com';
            var url2 = "http://example.com";
        </script>
        """
        try:
            minify_code(sample_code)
        except ValueError:
            self.fail("minify_code() raised ValueError unexpectedly with HTTP/HTTPS URLs!")

    def test_mismatched_curly_braces_throws(self):
        sample_code = """
        <script>
            function test() {
                var x = 5;
            /* missing closing brace */
        </script>
        """
        with self.assertRaises(ValueError) as ctx:
            minify_code(sample_code)
        self.assertIn("Mismatched curly braces", str(ctx.exception))

    def test_mismatched_parentheses_throws(self):
        sample_code = """
        <script>
            (function() {
                var x = 5;
            } )();
            (function( {
                var y = 10;
            } )();
        </script>
        """
        with self.assertRaises(ValueError) as ctx:
            minify_code(sample_code)
        self.assertIn("Mismatched parentheses", str(ctx.exception))

    def test_smiley_bug_sequences_throw(self):
        # Test }) throws
        sample_code1 = """
        <script>
            (function() {
                var x = 5;
            })();
        </script>
        """
        with self.assertRaises(ValueError) as ctx1:
            minify_code(sample_code1)
        self.assertIn("smiley-triggering sequence '})'", str(ctx1.exception))

        # Test 8) throws
        sample_code2 = """
        <script>
            if (precisionId === 8) {
                return 'Decade';
            }
        </script>
        """
        with self.assertRaises(ValueError) as ctx2:
            minify_code(sample_code2)
        self.assertIn("smiley-triggering sequence '8)'", str(ctx2.exception))

if __name__ == '__main__':
    unittest.main()
