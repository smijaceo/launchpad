#!/usr/bin/env bash
# Lighthouse (mobile preset) for each path; prints category scores; fails below 0.90.
# Usage: qa/lighthouse.sh <base_url> <out_dir> paths...
set -euo pipefail
base=$1; out=$2; shift 2; mkdir -p "$out"; fail=0
chrome=${CHROME_PATH:-/opt/pw-browsers/chromium}
for p in "$@"; do
  name=$(echo "$p" | tr '/' '_'); [ "$name" = "_" ] && name=home
  CHROME_PATH=$chrome npx --yes lighthouse@12.6.1 "$base$p" --quiet --chrome-flags="--headless=new --no-sandbox" \
    --only-categories=performance,accessibility,best-practices,seo --output=json --output-path="$out/$name.json" >/dev/null 2>&1 || true
  python3 - "$out/$name.json" "$p" <<'PY' || fail=1
import json,sys
r=json.load(open(sys.argv[1])); c=r["categories"]
s={k:round(v["score"]*100) for k,v in c.items()}
print(sys.argv[2], s)
sys.exit(0 if min(s[k] for k in ("performance","accessibility","seo"))>=90 else 1)
PY
done
exit $fail
