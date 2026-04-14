"""
UCSAT — Unit Communications Security Assessment Tool
Version 2.0 | Army ROTC
Author: Miguel Sevilla | github.com/mikelobocyber

No dependencies — Python 3 standard library only.
Run: python ucsat.py
"""

import os
import sys
import time
import datetime

# ── ANSI colors ────────────────────────────────────────────────────────────────
R   = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
BLK  = "\033[30m"
GRN  = "\033[32m"
YLW  = "\033[33m"
RED  = "\033[31m"
BLU  = "\033[34m"
CYN  = "\033[36m"
WHT  = "\033[37m"
BGRN = "\033[92m"
BYLW = "\033[93m"
BRED = "\033[91m"
BCYN = "\033[96m"
BWHT = "\033[97m"

W = 68  # terminal width

# ── Assessment data ─────────────────────────────────────────────────────────────
CATEGORIES = [
    {
        "id": "A",
        "name": "PACE Plan & Communication Redundancy",
        "weight": 1.5,
        "items": [
            "Unit has a documented, current PACE plan (Primary / Alternate / Contingency / Emergency)",
            "All assigned Soldiers can recite the full PACE plan without reference",
            "Alternate comms method tested within the last 30 days",
            "Emergency comms (runner, visual signals, hand-held radio) rehearsed this quarter",
            "PACE plan is updated after every major personnel or equipment change",
        ],
    },
    {
        "id": "B",
        "name": "Encryption & Authentication",
        "weight": 2.0,
        "items": [
            "All voice radio traffic uses proper COMSEC procedures (no clear-text on sensitive nets)",
            "COMSEC keys are current — no expired or compromised fills in use",
            "Passwords on all government-issued devices meet Army complexity requirements",
            "Multi-factor authentication is enabled on all accounts where available",
            "No shared or default passwords remain on any unit device or network resource",
        ],
    },
    {
        "id": "C",
        "name": "Device & Network Hygiene",
        "weight": 1.5,
        "items": [
            "Personal devices are prohibited from and not connected to unit tactical networks",
            "All government devices have OS and firmware patched within the last 90 days",
            "No unauthorized or unvetted applications installed on government equipment",
            "Physical access to communication equipment is controlled (locked, logged, or guarded)",
            "Removable media (USB drives, SD cards) use is controlled and tracked per SOP",
        ],
    },
    {
        "id": "D",
        "name": "OPSEC & Information Control",
        "weight": 1.5,
        "items": [
            "All Soldiers have received a unit OPSEC brief within the last 90 days",
            "No sensitive unit information (location, schedule, personnel) posted on personal social media",
            "Unit movement, timelines, and mission-relevant information is distributed on a need-to-know basis",
            "Radio call signs, frequencies, and crypto schedules are rotated per unit SOP",
            "Soldiers can identify and report a suspected OPSEC violation through proper channels",
        ],
    },
    {
        "id": "E",
        "name": "Wireless & RF Threat Awareness",
        "weight": 1.0,
        "items": [
            "Unit leaders are briefed on SIGINT and direction-finding threats in the current AO",
            "Minimize-radio discipline is enforced and rehearsed for sensitive operations",
            "Wi-Fi and Bluetooth use is restricted or disabled in tactical environments",
            "Soldiers can identify indicators of RF jamming and know the reporting procedure",
            "No consumer Wi-Fi routers or personal hotspots are used on unit networks",
        ],
    },
]

RISK_LEVELS = [
    (0.0,  25.0,  BGRN, "LOW",      "Maintain current posture. Conduct routine monthly reviews."),
    (25.0, 50.0,  BYLW, "MEDIUM",   "Address gaps within 30 days. Brief commander on findings."),
    (50.0, 75.0,  YLW,  "HIGH",     "Immediate corrective action required. Brief chain of command."),
    (75.0, 101.0, BRED, "CRITICAL", "Halt affected operations until vulnerabilities are closed."),
]


# ── UI helpers ──────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def bar(char="─", color=DIM, width=W):
    print(color + char * width + R)


def header():
    clear()
    bar("═", BOLD + CYN)
    print(BOLD + BCYN + "  UCSAT — Unit Communications Security Assessment Tool".center(W) + R)
    print(DIM + "  v2.0  |  Army ROTC  |  github.com/mikelobocyber".center(W) + R)
    bar("═", BOLD + CYN)
    print()


def prompt_yn(question):
    while True:
        ans = input(BOLD + BWHT + "  " + question + R + DIM + "  [y/n] → " + R).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print(DIM + "  Enter y or n." + R)


def slow_print(text, delay=0.018):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ── Scoring ─────────────────────────────────────────────────────────────────────
def score_to_risk(pct):
    for lo, hi, color, label, action in RISK_LEVELS:
        if lo <= pct < hi:
            return color, label, action
    return BRED, "CRITICAL", RISK_LEVELS[-1][4]


def risk_bar(pct, width=40):
    filled = int(round(pct / 100 * width))
    color, label, _ = score_to_risk(pct)
    bar_str = color + "█" * filled + DIM + "░" * (width - filled) + R
    return bar_str


# ── Intro ───────────────────────────────────────────────────────────────────────
def intro():
    header()
    slow_print(BOLD + BWHT + "  Welcome, Cadet." + R, 0.03)
    print()
    print("  This tool walks you through a structured communications security")
    print("  assessment for your unit. Answer each question honestly based on")
    print("  your unit's actual current posture — not what you plan to fix.")
    print()
    print(DIM + "  5 categories  ·  25 checklist items  ·  weighted risk scoring" + R)
    print(DIM + "  A full report will be saved to disk when you finish." + R)
    print()
    bar()
    print()
    unit = input(BOLD + "  Unit designation (e.g. 1st PLT, A CO): " + R).strip() or "Unknown Unit"
    assessor = input(BOLD + "  Your name / rank: " + R).strip() or "Unknown"
    print()
    return unit, assessor


# ── Category assessment ─────────────────────────────────────────────────────────
def run_category(cat, cat_num, total_cats):
    header()
    print(BOLD + BCYN + f"  Category {cat['id']} of {total_cats}  —  {cat['name']}" + R)
    print(DIM + f"  Weight: ×{cat['weight']}  ·  {len(cat['items'])} items" + R)
    print()
    bar()
    print()

    results = []
    for i, item in enumerate(cat["items"], 1):
        print(BOLD + f"  [{cat['id']}{i}]" + R + f"  {item}")
        passed = prompt_yn("PASS?")
        results.append(passed)
        if passed:
            print(BGRN + "       ✓ PASS" + R)
        else:
            print(BRED + "       ✗ FAIL  — flagged for report" + R)
        print()

    passed_count = sum(results)
    fail_count = len(results) - passed_count
    cat_pct = (fail_count / len(results)) * 100

    print()
    bar("─", DIM)
    print(BOLD + f"  Category {cat['id']} summary: " + R +
          BGRN + f"{passed_count} pass" + R + "  " +
          BRED + f"{fail_count} fail" + R +
          DIM + f"  ({cat_pct:.0f}% fail rate)" + R)
    bar("─", DIM)
    print()
    try:
        input(DIM + "  Press Enter to continue →" + R)
    except EOFError:
        pass

    return results


# ── Final report ────────────────────────────────────────────────────────────────
def build_report(unit, assessor, all_results):
    now = datetime.datetime.now()

    # weighted score
    total_weight = 0
    weighted_fail = 0
    category_summaries = []

    for cat, results in zip(CATEGORIES, all_results):
        fail_count = sum(1 for r in results if not r)
        pass_count = sum(results)
        cat_fail_pct = (fail_count / len(results)) * 100
        weighted_fail += cat_fail_pct * cat["weight"]
        total_weight += cat["weight"]
        category_summaries.append((cat, results, fail_count, pass_count, cat_fail_pct))

    overall_pct = weighted_fail / total_weight
    risk_color, risk_label, risk_action = score_to_risk(overall_pct)

    # ── Screen report ──────────────────────────────────────────────────────────
    header()
    print(BOLD + BCYN + "  ASSESSMENT COMPLETE — RISK REPORT".center(W) + R)
    print()
    bar("═", BOLD + CYN)
    print()
    print(BOLD + f"  Unit:       {unit}" + R)
    print(BOLD + f"  Assessor:   {assessor}" + R)
    print(BOLD + f"  Date/Time:  {now.strftime('%d %b %Y  %H:%M')}" + R)
    print()
    bar()
    print()

    # category breakdown
    print(BOLD + BWHT + "  CATEGORY BREAKDOWN" + R)
    print()
    for cat, results, fail_count, pass_count, cat_fail_pct in category_summaries:
        color, label, _ = score_to_risk(cat_fail_pct)
        status_str = color + BOLD + f"[{label:<8}]" + R
        fail_items = [cat["items"][i] for i, r in enumerate(results) if not r]
        print(f"  {BOLD}{cat['id']}.{R} {cat['name']:<40} {status_str}  "
              + BRED + f"{fail_count} fail" + R + DIM + f" / {len(results)} total" + R)
        for item in fail_items:
            truncated = item if len(item) <= 58 else item[:55] + "..."
            print(DIM + f"       ✗  {truncated}" + R)
        if fail_items:
            print()

    bar()
    print()

    # overall score
    print(BOLD + BWHT + "  OVERALL RISK SCORE" + R)
    print()
    print(f"  {risk_bar(overall_pct)}  {risk_color}{BOLD}{overall_pct:.1f}%{R}")
    print()
    print(f"  Risk Level:  {risk_color}{BOLD}{risk_label}{R}")
    print(f"  Action:      {risk_action}")
    print()
    bar("═", BOLD + CYN)

    # ── File report ────────────────────────────────────────────────────────────
    filename = f"ucsat_report_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    lines = []
    lines.append("=" * 68)
    lines.append("UCSAT — Unit Communications Security Assessment Report")
    lines.append("=" * 68)
    lines.append(f"Unit:       {unit}")
    lines.append(f"Assessor:   {assessor}")
    lines.append(f"Date/Time:  {now.strftime('%d %b %Y  %H:%M:%S')}")
    lines.append(f"Tool:       UCSAT v2.0 | github.com/mikelobocyber")
    lines.append("")
    lines.append("CATEGORY RESULTS")
    lines.append("-" * 68)

    for cat, results, fail_count, pass_count, cat_fail_pct in category_summaries:
        _, label, _ = score_to_risk(cat_fail_pct)
        lines.append(f"\n[{cat['id']}] {cat['name']}  —  [{label}]  ({fail_count} fail / {len(results)} total)")
        for i, (item, passed) in enumerate(zip(cat["items"], results), 1):
            status = "PASS" if passed else "FAIL"
            lines.append(f"  {cat['id']}{i}. [{status}]  {item}")

    lines.append("")
    lines.append("=" * 68)
    lines.append(f"OVERALL RISK SCORE:  {overall_pct:.1f}%  —  {risk_label}")
    lines.append(f"ACTION REQUIRED:     {risk_action}")
    lines.append("=" * 68)
    lines.append("")
    lines.append("NOTE: This tool was built with AI assistance (Claude / Anthropic).")
    lines.append("All outputs should be reviewed by the unit S6 before action.")

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print()
    print(BGRN + f"  Report saved → {filename}" + R)
    print()

    return filename


# ── Main ─────────────────────────────────────────────────────────────────────────
def main():
    try:
        unit, assessor = intro()

        all_results = []
        for cat in CATEGORIES:
            results = run_category(cat, cat["id"], len(CATEGORIES))
            all_results.append(results)

        build_report(unit, assessor, all_results)

        print(DIM + "  UCSAT v2.0  ·  Army ROTC  ·  github.com/mikelobocyber" + R)
        print()

    except KeyboardInterrupt:
        print()
        print()
        print(DIM + "  Assessment cancelled." + R)
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
