import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ieee-acm-paper-writing"
CHECKER = SKILL / "scripts" / "check_claims.py"
EXAMPLE = SKILL / "examples" / "claim-ledger.json"
SPEC = importlib.util.spec_from_file_location("check_claims", CHECKER)
CHECK = importlib.util.module_from_spec(SPEC)
PREVIOUS_DONT_WRITE_BYTECODE = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    SPEC.loader.exec_module(CHECK)
finally:
    sys.dont_write_bytecode = PREVIOUS_DONT_WRITE_BYTECODE

QUOTE = "the path between any input and output token is largely independent of the distance"


def tiny_pdf(lines):
    """Build a one-page PDF with Helvetica text lines (standard library only)."""
    ops = ["BT /F1 11 Tf 72 720 Td 14 TL"]
    for line in lines:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        ops.append(f"({escaped}) Tj T*")
    ops.append("ET")
    stream = "\n".join(ops).encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def literature(**evidence):
    return {"id": "C1", "text": "claim", "location": "Sec. I", "type": "literature",
            "evidence": [evidence], "judgment": "partial"}


class SchemaTests(unittest.TestCase):
    def test_bundled_example_validates(self):
        CHECK.validate_ledger(json.loads(EXAMPLE.read_text(encoding="utf-8")))

    def test_rejects_agent_stamped_level(self):
        claim = literature(cite_key="k1")
        claim["level"] = "quote-anchored"
        with self.assertRaisesRegex(CHECK.LedgerError, "may not set: level"):
            CHECK.validate_ledger({"version": 1, "claims": [claim]})

    def test_rejects_short_quote_and_quote_without_pdf(self):
        with self.assertRaisesRegex(CHECK.LedgerError, "at least 6 words"):
            CHECK.validate_ledger({"version": 1, "claims": [
                literature(cite_key="k1", source_pdf="a.pdf", quote="largely independent")]})
        with self.assertRaisesRegex(CHECK.LedgerError, "requires source_pdf"):
            CHECK.validate_ledger({"version": 1, "claims": [literature(cite_key="k1", quote=QUOTE)]})

    def test_rejects_unknown_judgment_and_duplicate_ids(self):
        claim = literature(cite_key="k1")
        claim["judgment"] = "verified"
        with self.assertRaisesRegex(CHECK.LedgerError, "judgment"):
            CHECK.validate_ledger({"version": 1, "claims": [claim]})
        with self.assertRaisesRegex(CHECK.LedgerError, "unique"):
            CHECK.validate_ledger({"version": 1, "claims": [literature(cite_key="k1")] * 2})


class MatchTests(unittest.TestCase):
    def test_match_levels(self):
        self.assertEqual(CHECK.match_level("a  b c", "x a b\nc y"), "exact")
        self.assertEqual(CHECK.match_level("largely independent", "Largely inde-\npendent"), "normalized")
        self.assertEqual(CHECK.match_level("only O(n/k) operations", "only O( nk ) operations"), "weak")
        self.assertEqual(CHECK.match_level("reduces complexity to O(n)", "unrelated text"), "none")


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        (self.base / "refs.bib").write_text("@article{k1,\n title={T}}\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, claim, have_pdftotext=False):
        ledger = CHECK.validate_ledger({"version": 1, "bib": "refs.bib", "claims": [claim]})
        return CHECK.check_ledger(ledger, self.base, have_pdftotext=have_pdftotext)[0]

    def test_missing_bib_key_fails(self):
        self.assertEqual(self.run_check(literature(cite_key="absent"))["level"], "key-missing")

    def test_quote_not_checked_without_pdftotext_stays_cited(self):
        (self.base / "s.pdf").write_bytes(b"%PDF-1.4")
        row = self.run_check(literature(cite_key="k1", source_pdf="s.pdf", quote=QUOTE))
        self.assertEqual(row["level"], "cited")
        self.assertIn("not-checked", row["evidence"][0]["note"])
        self.assertEqual(row["support"], "model-judged: partial; human confirmation pending")

    def test_empty_evidence_is_unresolved_and_assumption_is_labelled(self):
        claim = literature(cite_key="k1")
        claim["evidence"] = []
        self.assertEqual(self.run_check(claim)["level"], "unresolved")
        assumption = {"id": "A1", "text": "t", "location": "l", "type": "assumption",
                      "evidence": [], "judgment": "not-assessed"}
        self.assertEqual(self.run_check(assumption)["level"], "assumption")

    def test_own_result_value_match_respects_number_boundaries(self):
        (self.base / "r.csv").write_text("method,acc\nours,92.45\nbase,94.2\n", encoding="utf-8")
        claim = {"id": "R1", "text": "t", "location": "l", "type": "own-result",
                 "evidence": [{"artifact": "r.csv", "value": "94.2"}], "judgment": "not-assessed"}
        self.assertEqual(self.run_check(claim)["level"], "value-matched")
        claim["evidence"][0]["value"] = "92.4"
        self.assertEqual(self.run_check(claim)["level"], "value-mismatch")

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext not installed")
    def test_quote_checked_against_real_pdf(self):
        (self.base / "s.pdf").write_bytes(tiny_pdf([
            "Dependencies over long ranges are learnt easily because",
            "the path between any input and output token is largely",
            "independent of the distance between the tokens.",
        ]))
        anchored = self.run_check(literature(cite_key="k1", source_pdf="s.pdf", page=1, quote=QUOTE),
                                  have_pdftotext=True)
        self.assertEqual(anchored["level"], "quote-anchored")
        invented = literature(cite_key="k1", source_pdf="s.pdf", page=1,
                              quote="separable layers reduce the complexity to linear time")
        self.assertEqual(self.run_check(invented, have_pdftotext=True)["level"], "quote-mismatch")


class EvalFixtureTests(unittest.TestCase):
    """The claims eval cases point agents at these files; keep their checker outcomes fixed."""

    FIXTURES = ROOT / "evals" / "fixtures" / "claims"

    def check(self, claim):
        ledger = CHECK.validate_ledger({"version": 1, "bib": "refs.bib", "claims": [claim]})
        return CHECK.check_ledger(ledger, self.FIXTURES)[0]["level"]

    def test_csv_fixture_matches_one_value_and_rejects_the_other(self):
        claim = {"id": "R1", "text": "t", "location": "l", "type": "own-result",
                 "evidence": [{"artifact": "utilization.csv", "value": "94.2"}],
                 "judgment": "not-assessed"}
        self.assertEqual(self.check(claim), "value-mismatch")
        claim["evidence"][0]["value"] = "88.1"
        self.assertEqual(self.check(claim), "value-matched")

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext not installed")
    def test_pdf_fixture_anchors_its_scope_sentence(self):
        quote = ("For payloads up to 512 bytes, end-to-end delay over the two-hop relay chain "
                 "stayed within 3 ms of the single-hop value.")
        claim = literature(cite_key="relay2022", source_pdf="relay-delay-note.pdf", page=1, quote=quote)
        self.assertEqual(self.check(claim), "quote-anchored")


class CliTests(unittest.TestCase):
    def test_cli_exit_codes_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.json"
            ledger.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
            out = Path(tmp) / "report.json"
            self.assertEqual(CHECK.main([str(ledger), "--out", str(out)]), 0)
            levels = [row["level"] for row in json.loads(out.read_text())["claims"]]
            self.assertEqual(levels, ["cited", "unresolved", "assumption"])
            self.assertEqual(CHECK.main([str(ledger), "--out", str(out)]), 2)
            ledger.write_text("{}", encoding="utf-8")
            self.assertEqual(CHECK.main([str(ledger)]), 2)


if __name__ == "__main__":
    unittest.main()
