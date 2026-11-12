# Why Patients Miss Care — Research #1

**Student:** G11 안현빈 (DICS)
**Study:** Appointment Lead Time and Medical Appointment Attendance: An Observational Data Study
**Stage:** Kickoff / dataset verification pending. **No actual Kaggle CSV analysis has been run.**

## Main research question
Among medical appointments in the publicly available Brazilian dataset, how is booking-to-appointment lead time associated with recorded nonattendance?

This is a nursing-oriented observational project. It is not a clinical tool, patient-blame exercise, SMS effectiveness experiment or proof of causal impact.

## Dataset
Public Kaggle listing: https://www.kaggle.com/datasets/joniarroba/noshowappointments

Secondary descriptions suggest approximately 110,527 appointments and 14 columns collected in Brazil. These counts are NOT verified by the student's downloaded file. Verify the exact version, source and license before reporting findings.

## Local setup
1. Download the CSV legally via Kaggle to data/raw/appointments.csv.
2. Verify source and terms in docs/DATA_PROVENANCE.md.
3. Install and test locally:

    python -m venv .venv
    # Windows PowerShell: .venv\Scripts\Activate.ps1
    # macOS/Linux: source .venv/bin/activate
    pip install -r requirements.txt
    python -m unittest discover -s tests -v
    python -m src.attendance_analysis --input data/raw/appointments.csv --output outputs

Review outputs/quality_report.json BEFORE interpreting any aggregated analysis outputs. The raw data and outputs directories are ignored by Git and must not be committed without a privacy and licensing review.

## Repository structure
- docs/RESEARCH_PROTOCOL.md — questions, data definitions, assumptions, analysis plan, ethical limitations
- docs/DATA_PROVENANCE.md — source, version, license and file hash verification gate
- docs/DATA_DICTIONARY.md — candidate fields requiring verification
- docs/WEEK_01_PLAYBOOK.md — five student learning sessions and acceptance criteria
- docs/STATUS.md — documented state (planned vs run)
- docs/RESEARCH_JOURNAL.md — record of genuine student contributions
- research/01_student_question.md — student-authored rationale and hypotheses
- literature/evidence_matrix.csv — literature review template
- src/attendance_analysis.py — reproducible basic audit, descriptive rates and chart
- tests/ — synthetic examples only, not actual patient data
- .github/workflows/test.yml — checks on synthetic tests

## Research sequence
#1 Appointment Attendance: complete in depth first.
#3 Preventive Care Access and #4 Hospital Quality: launch in parallel after #1 methods stabilize.
#2 Diabetes Readmission: separate advanced study with substantial independent scope.

## Scientific integrity and clinical scope
- No real dataset results yet; synthetic test results do not constitute findings.
- No-show label mapping: Yes = missed, No = attended.
- Same patient can appear in multiple appointments; records are not independent patients.
- SMS status is observational, not evidence of a reminder's causal effectiveness.
- Lead-time differences use calendar dates; same-day appointments are not incorrectly negative.
- Patient privacy, dataset license and source quality must be verified.
- This scaffold was counselor/AI-assisted. Student must run, understand, review, critique and record individual contributions before presenting them as student research.

**Official source entry:** https://www.kaggle.com/datasets/joniarroba/noshowappointments
