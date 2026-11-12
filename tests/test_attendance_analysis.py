"""Synthetic tests only; passing does not validate the real dataset."""

import tempfile
import unittest
from pathlib import Path

import pandas as pd
from src.attendance_analysis import read_and_validate, run


class AttendanceTests(unittest.TestCase):
    def example(self, folder: Path) -> Path:
        cases = [
            ("A", "1", "2016-04-29T18:38:08Z", "2016-04-29T00:00:00Z", "No", 62, 0),
            ("A", "2", "2016-04-20T08:00:00Z", "2016-04-29T00:00:00Z", "Yes", 62, 1),
            ("B", "3", "2016-04-30T08:00:00Z", "2016-04-29T00:00:00Z", "Yes", 30, 0),
            ("C", "4", "2016-04-20T08:00:00Z", "2016-04-29T00:00:00Z", "Maybe", 20, 1),
            ("D", "5", "2016-04-20T08:00:00Z", "2016-04-29T00:00:00Z", "No", -1, 0),
        ]
        df = pd.DataFrame([{
            "PatientId": p, "AppointmentID": a, "Gender": "F",
            "ScheduledDay": s, "AppointmentDay": ap, "Age": age,
            "Neighbourhood": "TEST", "Scholarship": 0, "Hipertension": 0,
            "Diabetes": 0, "Alcoholism": 0, "Handcap": 0,
            "SMS_received": sms, "No-show": outcome,
        } for p, a, s, ap, outcome, age, sms in cases])
        file = folder / "synthetic.csv"
        df.to_csv(file, index=False)
        return file

    def test_quality_and_correct_outcome_mapping(self):
        with tempfile.TemporaryDirectory() as temp:
            rows, quality = read_and_validate(self.example(Path(temp)))
            self.assertEqual(quality["raw_rows"], 5)
            self.assertEqual(quality["included_rows"], 2)
            self.assertEqual(quality["excluded_any_reason"], 3)
            self.assertEqual(quality["patients_with_multiple_rows"], 1)
            self.assertEqual(rows["lead_days"].tolist(), [0, 9])
            self.assertEqual(rows["no_show"].tolist(), [0, 1])

    def test_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            output = folder / "out"
            summary = run(self.example(folder), output)
            self.assertEqual(summary["no_show_percentage"], 50.0)
            for name in ["quality_report.json", "overall_summary.json",
                         "lead_time_rates.csv", "age_group_rates.csv",
                         "sms_status_rates.csv", "lead_time_rates.png"]:
                self.assertTrue((output / name).is_file(), name)

    def test_missing_column_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "bad.csv"
            pd.DataFrame({"No-show": ["Yes"]}).to_csv(file, index=False)
            with self.assertRaisesRegex(ValueError, "missing expected columns"):
                read_and_validate(file)


if __name__ == "__main__":
    unittest.main()
