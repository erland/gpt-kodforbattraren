#!/usr/bin/env python3
import argparse, json, re

def classify(text: str) -> str:
    s = re.sub(r"\s+", " ", text.strip().lower())
    execute = {
        "gör nästa steg", "gor nasta steg", "fortsätt", "fortsatt", "nästa", "nasta",
        "gå vidare", "ga vidare", "gör nästa", "gor nasta"
    }
    status = {"vad är nästa steg?", "vad är nästa steg", "vad ar nasta steg?", "vad ar nasta steg", "visa status", "status"}
    if s in execute:
        return "execute_next_step"
    if s in status:
        return "show_next_step" if "nästa steg" in s or "nasta steg" in s else "show_status"
    if "fortsätt med pr" in s or "fortsatt med pr" in s:
        return "continue_github_pr"
    return "normal_request"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('text')
    args=ap.parse_args()
    print(json.dumps({'intent': classify(args.text)}, ensure_ascii=False))

if __name__=='__main__': main()
