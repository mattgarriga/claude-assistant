import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import time_entry as t

SAMPLE = """Ethos - General: 2.5 |

* Day planning | Dev huddle

IMI - 26-08192: .25 |

* Multi-position budget setup fixes
"""


class TimeEntry(unittest.TestCase):
    def test_parse(self):
        e = t.parse(SAMPLE)
        self.assertEqual(len(e), 2)
        self.assertEqual((e[1]["client"], e[1]["label"], e[1]["hours_raw"]), ("IMI", "26-08192", 0.25))
        self.assertEqual(e[0]["tasks"], ["Day planning", "Dev huddle"])

    def test_reconcile_to_quarter_total(self):
        rows = [{"hours_raw": 2.4, "hours": 2.4}, {"hours_raw": 0.8, "hours": 0.8}]
        self.assertEqual(t.reconcile(rows), 3.25)
        self.assertEqual(sum(r["hours"] for r in rows), 3.25)

    def test_unparsed_line_reported(self):
        e = t.parse("random text\n")
        self.assertIn("unparsed", e[0])


if __name__ == "__main__":
    unittest.main()
