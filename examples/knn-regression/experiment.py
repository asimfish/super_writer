#!/usr/bin/env python3
"""Reproduce a small, synthetic nearest-neighbor regression experiment offline."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import random
import statistics

SEEDS = (11, 22, 33, 44, 55)
TRAIN_SIZE = 40
TEST_SIZE = 101
NOISE = 0.5


def signal(x: float) -> float:
    return 2.0 * x + math.sin(4.0 * math.pi * x)


def predict(training: list[tuple[float, float]], x: float, k: int) -> float:
    if not 1 <= k <= len(training):
        raise ValueError("k must be between 1 and the training set size")
    neighbors = sorted(enumerate(training), key=lambda item: (abs(item[1][0] - x), item[0]))[:k]
    return statistics.mean(pair[1] for _, pair in neighbors)


def run() -> tuple[list[dict], dict]:
    rows = []
    for seed in SEEDS:
        generator = random.Random(seed)
        training = []
        for _ in range(TRAIN_SIZE):
            x = generator.random()
            training.append((x, signal(x) + generator.uniform(-NOISE, NOISE)))
        for domain, offset in (("in_domain", 0.0), ("extrapolation", 1.0)):
            points = [offset + (i + 0.5) / TEST_SIZE for i in range(TEST_SIZE)]
            for k in (1, 5):
                errors = [(predict(training, x, k) - signal(x)) ** 2 for x in points]
                rows.append({"seed": seed, "domain": domain, "k": k, "mse": statistics.mean(errors)})
    aggregates = []
    for domain in ("in_domain", "extrapolation"):
        for k in (1, 5):
            values = [row["mse"] for row in rows if row["domain"] == domain and row["k"] == k]
            aggregates.append({"domain": domain, "k": k, "mean_mse": statistics.mean(values),
                               "sample_sd": statistics.stdev(values)})
    return rows, {
        "data_kind": "synthetic function and noise; measured program outputs, not real-world observations",
        "seeds": list(SEEDS), "train_size": TRAIN_SIZE, "test_size_per_domain": TEST_SIZE,
        "noise_uniform": [-NOISE, NOISE], "aggregation": "mean and sample SD across training seeds",
        "results": aggregates,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Explicit directory for results.csv and summary.json")
    args = parser.parse_args()
    rows, summary = run()
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with (args.output_dir / "results.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=("seed", "domain", "k", "mse"), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
