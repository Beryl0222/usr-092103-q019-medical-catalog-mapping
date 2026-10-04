import json
import unittest
from pathlib import Path

from src.validator import validate_event

ROOT = Path(__file__).parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ContractTest(unittest.TestCase):
    def test_sample_matches_envelope(self) -> None:
        self.assertEqual(validate_event(load(ROOT / "data" / "sample.json")), [])

    def test_samples_directory_matches_envelope(self) -> None:
        paths = sorted((ROOT / "data" / "samples").glob("*.json"))
        self.assertTrue(paths, "data/samples 下应至少有一条样例")
        for path in paths:
            with self.subTest(sample=path.name):
                self.assertEqual(validate_event(load(path)), [])


class ValidatorTest(unittest.TestCase):
    def base_event(self) -> dict:
        return load(ROOT / "data" / "sample.json")

    def test_unknown_event_type_rejected(self) -> None:
        event = self.base_event() | {"event_type": "SOMETHING_ELSE"}
        self.assertIn("未登记的事件类型：SOMETHING_ELSE", validate_event(event))

    def test_unknown_aggregate_type_rejected(self) -> None:
        event = self.base_event() | {"aggregate_type": "unknown"}
        self.assertIn("未登记的聚合类型：unknown", validate_event(event))

    def test_version_must_be_positive_int(self) -> None:
        for bad in (0, -1, "2", True):
            with self.subTest(version=bad):
                event = self.base_event() | {"version": bad}
                self.assertIn("version 必须是正整数", validate_event(event))

    def test_occurred_at_must_be_datetime(self) -> None:
        event = self.base_event() | {"occurred_at": "昨天"}
        self.assertIn("occurred_at 必须是 ISO 8601 日期时间", validate_event(event))

    def test_empty_summary_rejected(self) -> None:
        event = self.base_event() | {"summary": "  "}
        self.assertIn("summary 必须是非空字符串", validate_event(event))


if __name__ == "__main__":
    unittest.main()
