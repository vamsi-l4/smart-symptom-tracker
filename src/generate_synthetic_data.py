#!/usr/bin/env python3
"""
generate_synthetic_data.py
Generates synthetic symptom descriptions and triage labels.

Usage:
  python generate_synthetic_data.py --n 5000 --out ../data/raw.csv --seed 42 --balance balanced

Outputs CSV with columns: id,text,label
Labels: self-monitor, doctor, urgent-care, emergency
"""
import random
import argparse
import csv
from datetime import timedelta, date

random.seed(42)

SYM_COMMON = [
    "headache", "sore throat", "runny nose", "stuffy nose", "mild cough",
    "sneezing", "fatigue", "tiredness", "low fever", "chills", "muscle ache",
    "nausea", "mild stomach pain", "diarrhea", "itchy eyes", "watery eyes",
    "back ache", "joint pain", "dizziness", "lightheadedness"
]

SYM_DOCTOR = [
    "high fever", "persistent fever", "strong cough", "productive cough",
    "sinus pain", "ear pain", "severe sore throat", "worsening cough",
    "abdominal pain", "vomiting", "blood in stool", "significant weight loss",
    "new lump", "persistent bleeding", "vision changes"
]

SYM_URGENT = [
    "moderate chest pain", "difficulty breathing", "worsening shortness of breath",
    "sudden dizziness", "severe vomiting", "high fever with rash",
    "dehydration", "confusion", "fainting", "severe abdominal pain"
]

SYM_EMERGENCY = [
    "severe chest pain", "difficulty breathing", "unconscious", "severe bleeding",
    "suspected stroke", "slurred speech", "one-sided weakness", "sudden confusion",
    "seizure", "very low blood pressure", "severe head trauma", "airway obstruction"
]

SEVERITIES = ["mild", "moderate", "severe", "slight", "intense"]
DURATIONS = ["for 1 day", "for 2 days", "for 3 days", "for a week", "since yesterday", "since this morning", "for several hours", "intermittently"]
AGE_PHRASES = [
    "I am 25 years old", "A 40-year-old", "I'm 62", "Age 18", "A child aged 8", "A 70-year-old"
]
ONSET = ["started suddenly", "started gradually", "woke up with", "began after eating", "after exercise", "after the accident"]

# helper functions
def pick_one(lst):
    return random.choice(lst)

def maybe(prefix, prob=0.4):
    return prefix if random.random() < prob else ""

def compose_self_monitor():
    parts = []
    if random.random() < 0.6:
        parts.append(maybe(pick_one(AGE_PHRASES), prob=0.3))
    parts.append(pick_one(SYM_COMMON))
    if random.random() < 0.5:
        parts.append(maybe(pick_one(DURATIONS), prob=0.9))
    if random.random() < 0.4:
        parts.append("no shortness of breath or chest pain")
    return " ".join([p for p in parts if p])

def compose_doctor():
    parts = []
    parts.append(maybe(pick_one(AGE_PHRASES), prob=0.3))
    parts.append(pick_one(SYM_DOCTOR))
    # add an extra symptom sometimes
    if random.random() < 0.7:
        parts.append("and " + pick_one(SYM_COMMON))
    parts.append(pick_one(DURATIONS))
    if random.random() < 0.3:
        parts.append("symptoms are getting worse")
    return " ".join([p for p in parts if p])

def compose_urgent():
    parts = []
    if random.random() < 0.5:
        parts.append(maybe(pick_one(AGE_PHRASES), prob=0.4))
    parts.append(pick_one(SYM_URGENT))
    if random.random() < 0.6:
        parts.append("started " + pick_one(DURATIONS).replace("for ", ""))
    if random.random() < 0.4:
        parts.append("need urgent check")
    return " ".join([p for p in parts if p])

def compose_emergency():
    # emergency sentences are short/direct and include red flags
    parts = []
    parts.append(pick_one(SYM_EMERGENCY))
    if random.random() < 0.5:
        parts.append("started suddenly")
    if random.random() < 0.4:
        parts.append("loss of consciousness" if random.random() < 0.2 else "call emergency services")
    return " ".join([p for p in parts if p])

def injury_or_accident_noise():
    phrases = [
        "after a fall", "following a car accident", "after a sports injury", "sustained blunt trauma",
        "hit head on the floor", "cut while working"
    ]
    return pick_one(phrases)

def generate_row(label):
    if label == "self-monitor":
        text = compose_self_monitor()
    elif label == "doctor":
        text = compose_doctor()
    elif label == "urgent-care":
        text = compose_urgent()
    elif label == "emergency":
        text = compose_emergency()
    else:
        text = "unspecified symptom"
    # include some noise and variation
    if random.random() < 0.12:
        # add an onset phrase
        text = f"{pick_one(ONSET)}: {text}"
    if random.random() < 0.05:
        # add injury context sometimes
        text = f"{text} {injury_or_accident_noise()}"
    # small text cleanups
    text = text.strip()
    # avoid empty
    if not text:
        text = pick_one(SYM_COMMON)
    return text

def build_counts(total, mode="balanced"):
    # determine counts per class
    if mode == "balanced":
        per = total // 4
        counts = {
            "self-monitor": per,
            "doctor": per,
            "urgent-care": per,
            "emergency": per
        }
        # add remainder to self-monitor
        rem = total - per*4
        counts["self-monitor"] += rem
    elif mode == "realistic":
        # more mild cases than emergencies (example distribution)
        counts = {
            "self-monitor": int(total * 0.6),
            "doctor": int(total * 0.2),
            "urgent-care": int(total * 0.15),
            "emergency": int(total * 0.05),
        }
    else:  # all balanced fallback
        per = total // 4
        counts = {k: per for k in ["self-monitor","doctor","urgent-care","emergency"]}
    return counts

def main(args):
    total = args.n
    random.seed(args.seed)
    counts = build_counts(total, mode=args.balance)
    rows = []
    id_counter = 1
    for label, cnt in counts.items():
        for _ in range(cnt):
            text = generate_row(label)
            # small variation in punctuation
            if random.random() < 0.25:
                if not text.endswith("."):
                    text = text + "."
            # occasionally uppercase first letter
            if random.random() < 0.4:
                text = text[0].upper() + text[1:]
            rows.append((id_counter, text, label))
            id_counter += 1

    # shuffle rows
    random.shuffle(rows)

    # write CSV
    outpath = args.out
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id","text","label"])
        for r in rows:
            writer.writerow(r)
    print(f"Wrote {len(rows)} rows to {outpath}")
    # print class counts for quick check
    from collections import Counter
    labels = [r[2] for r in rows]
    print("Label distribution after shuffle:", Counter(labels))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5000, help="Total number of rows to generate")
    parser.add_argument("--out", type=str, default="../data/raw.csv", help="Output CSV path (relative to src/)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--balance", type=str, default="balanced", choices=["balanced","realistic"], help="Class distribution")
    args = parser.parse_args()
    main(args)
