#!/usr/bin/env python3
"""Deterministisk beslutsfunktion för Kodförbättrarens GitHub-läge."""
import argparse, json


def decide(s):
    if s.get("relevant_base_change"):
        return "reanalysis_required"
    if s.get("conflict_or_unclear_divergence"):
        return "blocked_conflict_or_divergence"
    pr_state = s.get("active_pr_state")
    if pr_state == "open":
        if s.get("same_plan", True) and s.get("relevant_branch", True):
            return "continue_open_pr"
        return "blocked_conflict_or_divergence"
    if pr_state == "merged":
        return "create_new_pr_after_merge"
    if pr_state == "closed":
        return "blocked_closed_unmerged"
    return "create_first_pr"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("state_json")
    args = ap.parse_args()
    with open(args.state_json, encoding="utf-8") as f:
        state = json.load(f)
    print(decide(state))

if __name__ == "__main__":
    main()
