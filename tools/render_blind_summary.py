#!/usr/bin/env python3
"""Render an aggregated blind-review JSON as a cautious HTML report."""

import argparse
import html
import json
from pathlib import Path


def verdict(summary):
    reviewers = summary.get("reviewers", 0)
    preferences = summary.get("preferences", {})
    if reviewers < 2:
        return "INSUFFICIENT EVIDENCE: fewer than two independent reviewers."
    if preferences.get("old", 0) and preferences.get("new", 0):
        return "MIXED EVIDENCE: preferences favor neither version uniformly."
    if preferences.get("tie", 0):
        return "CONDITIONAL: at least one tie or unresolved comparison remains."
    return "DIRECTIONAL EVIDENCE: preference is consistent, but this is not an acceptance predictor."


def render(summary):
    score_rows = []
    for dimension in ("contribution", "rationale", "precision", "evidence", "language"):
        old = summary["scores"]["old"][dimension]
        new = summary["scores"]["new"][dimension]
        score_rows.append(f"<tr><td>{html.escape(dimension)}</td><td>{old:.3f}</td><td>{new:.3f}</td><td>{new-old:+.3f}</td></tr>")
    case_rows = []
    for case_id, data in summary.get("per_case", {}).items():
        preference = ", ".join(f"{k}: {v}" for k, v in data["preferences"].items()) or "none"
        delta = "; ".join(f"{k}: {v:+.3f}" for k, v in data["delta_new_minus_old"].items())
        case_rows.append(f"<tr><td>{html.escape(case_id)}</td><td>{html.escape(preference)}</td><td>{html.escape(delta)}</td></tr>")
    agreement = summary.get("preference_agreement")
    agreement_text = "not available" if agreement is None else f"{agreement['exact_agreement']:.3f} ({agreement['agreements']}/{agreement['pairs']} pairs)"
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>Blind review summary</title>
<style>body{{font:15px/1.6 system-ui,sans-serif;max-width:1000px;margin:32px auto;padding:0 18px;color:#18212b}}table{{border-collapse:collapse;width:100%;margin:12px 0 26px}}th,td{{border:1px solid #d9dee5;padding:9px;text-align:left}}th{{background:#f4f6f8}}.verdict{{border-left:4px solid #176b87;background:#f1f8fa;padding:12px;margin:18px 0}}.muted{{color:#64707d}}</style>
<h1>Blind Abstract Review Summary</h1><p class="muted">Reviewers: {summary.get('reviewers', 0)} · Preference agreement: {agreement_text}</p>
<div class="verdict"><strong>{html.escape(verdict(summary))}</strong></div>
<h2>Dimension Scores</h2><table><tr><th>Dimension</th><th>Old</th><th>New</th><th>New - Old</th></tr>{''.join(score_rows)}</table>
<h2>Per-paper Results</h2><table><tr><th>Case</th><th>Preferences</th><th>Score deltas</th></tr>{''.join(case_rows)}</table>
<p class="muted">Scores describe this review sample only. They do not establish venue acceptance, human population preference, or universal writing improvement.</p></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(render(json.loads(args.summary.read_text())))
    print(args.output)


if __name__ == "__main__":
    main()
