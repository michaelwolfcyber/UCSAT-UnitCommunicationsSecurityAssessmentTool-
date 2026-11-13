# UCSAT — Unit Communications Security Assessment Tool

An educational command-line checklist that demonstrates weighted scoring for communications-security topics and saves a local assessment report. It is a personal learning project, not an official Army assessment, approved inspection instrument, or source of operational guidance.

Originally developed as an Army ROTC MS202 learning project | Python 3 | No dependencies

---

## Scope and safe use

Use only fictional examples and non-sensitive information. Do not enter real unit designations, personnel names, schedules, locations, communications plans, frequencies, call signs, cryptographic material, or other operational or controlled information. Reports are written to the local working directory and should be treated accordingly.

The checklist is illustrative and does not replace current Army policy, unit procedures, a qualified COMSEC/OPSEC review, or direction from the chain of command. Do not use its score as an authoritative security rating or compliance determination.

---

## Usage

```bash
python3 ucsat.py
```

The tool will ask for your unit designation and name, then walk you through 25 yes/no questions across five categories. When finished it prints a color-coded risk score and saves a `.txt` report file automatically.

---

## Categories

| # | Category |
|---|----------|
| A | Communication Redundancy Planning |
| B | Encryption & Authentication |
| C | Device & Network Hygiene |
| D | Information Security & OPSEC |
| E | Wireless & RF Threat Awareness |

Each category is weighted by criticality. The final score maps to one of four risk levels: **Low**, **Medium**, **High**, or **Critical**.

---

## Output

- Color-coded terminal output with per-category breakdown
- Overall weighted risk score with a visual progress bar
- Auto-saved plain-text report: `ucsat_report_YYYYMMDD_HHMMSS.txt`

---

## Requirements

- Python 3
- No installs or dependencies needed

