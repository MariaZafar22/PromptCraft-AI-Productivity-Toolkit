import io
import unittest
from contextlib import redirect_stdout

from ai_productivity_toolkit.cli import build_parser, main


class CLITests(unittest.TestCase):
    def run_cli(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["--mock", *argv])
        return code, buf.getvalue().strip()

    def test_summarize(self):
        code, out = self.run_cli("summarize", "Some long text.")
        self.assertEqual((code, out), (0, "[mock output]"))

    def test_classify_returns_known_label_or_unknown(self):
        code, out = self.run_cli("classify", "great!", "--labels", "positive,negative")
        self.assertEqual(code, 0)
        self.assertEqual(out, "unknown")  # mock output matches no label

    def test_email_accepts_repeated_points(self):
        code, _ = self.run_cli("email", "extension", "--point", "sick", "--point", "2 days")
        self.assertEqual(code, 0)

    def test_command_is_required(self):
        with self.assertRaises(SystemExit):
            build_parser().parse_args([])


if __name__ == "__main__":
    unittest.main()
