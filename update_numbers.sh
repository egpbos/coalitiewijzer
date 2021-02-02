#!/usr/bin/env sh
set -e
python update_numbers.py
python check_numbers.py
git add peilingen.pkl table.pkl last_updated.json
git commit -m "updated numbers from Peilingwijzer"
