# UCSAT — Unit Communications Security Assessment Tool

A command-line tool that walks unit leaders through a structured communications security assessment, scores their unit's posture in real time, and saves a report to disk.

Built for Army ROTC MS202 | Python 3 | No dependencies

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

