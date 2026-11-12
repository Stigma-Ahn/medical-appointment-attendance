# Research Protocol v0.1 — PRE-ANALYSIS

Student: G11 안현빈 (DICS)
Working title: Why Patients Miss Care: Medical Appointment Lead Time and Attendance
Study design: Secondary, observational; no randomized intervention, patient diagnosis or causal claim.
State: Working protocol. Document amendments after examining data.

## Rationale
Missed medical appointments may affect continuity of care. Nursing can involve preparation, patient education, communication and follow-up. Observational associations cannot tell us why an individual patient missed care or prove that a proposed communication intervention works.

## Primary research question
How is the number of WHOLE CALENDAR DAYS from scheduling to appointment associated with recorded nonattendance?

## Secondary questions
1. How does attendance differ by prespecified age groups?
2. How is recorded SMS status associated with no-show? This is NOT an effectiveness test.
3. Are recorded neighborhood comparisons meaningful given uncertain geographic definitions?
4. Do patterns differ for same-day bookings and appointments booked ahead?
5. How might these data inform ethically cautious questions about access and continuity of care?

## Hypotheses (NOT results)
H1: No-show proportions differ between booking lead-time categories.
H2: An association may persist after adjusting for measured covariates.
Exploratory: SMS status may correlate with no-show for reasons unrelated to reminders.

## Variables and unit of analysis
| Field | Plan | Important caution |
|---|---|---|
| Unit | Appointment | A patient can have multiple records |
| Outcome | No-show: Yes = missed (1); No = attended (0) | Explicit mapping, reject unknown labels |
| Primary exposure | lead_days = calendar date(AppointmentDay) - date(ScheduledDay) | Booking timestamp often later than visit midnight |
| Lead-time categories | 0; 1-7; 8-14; 15-30; 31+ | Defined ahead of analysis |
| Age categories | 0-17; 18-39; 40-64; 65+ | Flag extreme/invalid values |
| SMS_received | Recorded SMS status | Not randomized, timing uncertain |
| Scholarship | Welfare-related field | Not an income measure |
| Neighbourhood | Source locality field | Do not presume patient residence |

## Quality audit
1. Record actual CSV filename, SHA-256, file version, total rows/columns.
2. Inspect missing and unknown outcome labels, date parsing, negative calendar lead times, missing or negative age.
3. Inspect duplicate AppointmentID records and repeated PatientId values.
4. Flag age >115 for review (do not silently exclude).
5. For initial analysis exclude invalid outcome/date/lead/negative age, reporting EACH reason plus the combined union to avoid double-counting.
6. Do not silently impute, relabel, or invent missing values.

## Analysis
**Stage 1, in starter script:** Source audit; counts/denominators; no-show rates by prespecified lead group, age group, SMS status; noncausal descriptive figure.

**Stage 2, not implemented yet:** Confidence intervals; multi-variable logistic regression with measured confounder review; within-patient dependence; nonlinearity; sensitivity for extremes, repeated appointments and different modeling decisions.

**Stage 3, not implemented yet:** Literature comparison; RN/care communication implications; plain-language appointment guide prototype; ethical supervised nonclinical usability evaluation if justified.

## Limitations / bias
- Only scheduled appointments are observed, not people who never entered the appointment system.
- Reasons such as transport, work, caregiving or changing symptoms are generally not observed.
- SMS status may be selected by booking interval/clinic workflow; crude SMS differences are not causal.
- Repeated patients violate naive independence; account for this in later inference.
- Clinic vs residence meaning of neighborhood must be verified.
- Historical Brazil dataset cannot be generalized directly to Korea/USA.
- Labeling, measurement error, missingness, unobserved confounding.

## Stewardship
Public Kaggle listing does not automatically authorize republication of row-level data. Keep raw rows and identifiers out of GitHub. No claim of clinical partnerships, real patient feedback or proven intervention effects without appropriate documented permissions.

## Completion checklist
- [ ] License and original source verified
- [ ] Student downloads and independently examines CSV
- [ ] SHA and actual counts confirmed
- [ ] Student explains all exclusions and denominators
- [ ] Primary descriptive output reviewed
- [ ] Literature matrix contains verified papers
- [ ] Statistical analysis with assumptions and robustness documented
- [ ] Nursing reflection and scientific limitations reviewed
- [ ] Final report, poster and student-authored reflection
