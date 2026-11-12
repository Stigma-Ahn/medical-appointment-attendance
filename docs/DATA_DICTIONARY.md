# Candidate Data Dictionary — confirm with actual CSV

| Source field | Provisional interpretation | Quality or ethics caution |
|---|---|---|
| PatientId | Identifier of patient | May repeat; do not publish |
| AppointmentID | Appointment ID | Audit duplicate values |
| Gender | Recorded gender code | Inspect categories and meaning |
| ScheduledDay | Booking timestamp | Confirm from source |
| AppointmentDay | Appointment date | May have midnight time |
| Age | Age | Check invalid/extreme values |
| Neighbourhood | Named locality | Residence/clinic semantics not established |
| Scholarship | Welfare-program field | Not direct income |
| Hipertension | Source spelling of hypertension flag | Preserve original spelling |
| Diabetes | Disease flag | Not a validated diagnosis |
| Alcoholism | Administrative flag | Avoid stigma and unjustified claims |
| Handcap | Source spelling of disability flag | Confirm numerical category meaning |
| SMS_received | Recorded SMS status | Not random assignment |
| No-show | Yes=missed; No=attended | Explicit reverse-coding check |

Derived: lead_days = date(AppointmentDay)-date(ScheduledDay); categories 0, 1-7, 8-14, 15-30, 31+.  
Do not use this provisional dictionary as evidence of a verified data audit.
