# Week 1 Playbook — G11 Student Research

## Goal
Be able to explain one real public dataset, its provenance, an observational research question and the difference between correlation and causation.

### Session 1 (45-60 min): Nursing context
Read protocol. Write 100–150 words IN YOUR OWN VOICE in research/01_student_question.md. What is one appointment? Can a patient appear more than once? Why should missed care not be framed as a patient moral failure?

### Session 2 (45-60 min): Verify the source
Visit https://www.kaggle.com/datasets/joniarroba/noshowappointments. Identify original collector, documented license, source file, variables and download date. Fill docs/DATA_PROVENANCE.md truthfully. Never commit raw patient-level rows.

### Session 3 (45-60 min): Setup and synthetic tests
Windows PowerShell:
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python -m unittest discover -s tests -v

These tests check code logic on invented rows, not real study validity.

### Session 4 (60-90 min): First real dataset audit
Save authorized CSV locally: data/raw/appointments.csv
Run:
    python -m src.attendance_analysis --input data/raw/appointments.csv --output outputs

Read outputs/quality_report.json FIRST. Inspect invalid dates, duplicates, unusual ages, missing labels, included vs excluded counts. Review rates only after quality gate. Document hash and evidence.

### Session 5 (45-60 min): Interpretation
Explain outcome coding: No-show Yes means missed.
Why does SMS_received not prove messages caused attendance?
Why isn't a repeated PatientId a unique new patient?
What questions cannot be answered from this dataset?
Complete docs/RESEARCH_JOURNAL.md with specific student work and AI/counselor assistance.

## Week 1 acceptance
- [ ] Student explains hypotheses and unit of analysis
- [ ] Source version and license verified
- [ ] Student executes code on authorized CSV
- [ ] File hash and audit reviewed
- [ ] All exclusions and denominators documented
- [ ] Interpretations avoid causal or clinical overclaiming

Follow-on plan: Deep #1 -> initiate #3 Preventive Care / #4 Hospital Quality in parallel after methods stabilize -> separate #2 Diabetes Readmission advanced study.
