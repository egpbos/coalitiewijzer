#!/usr/bin/env sh
set -e
curl -s https://d1bjgq97if6urz.cloudfront.net/Public/Peilingwijzer/Last/Cijfers_Peilingwijzer.xlsx -o Cijfers_Peilingwijzer.xlsx
ls -l
python update_numbers.py
python check_numbers.py
git add peilingen.pkl table.pkl last_updated.json
git commit -m "updated numbers from Peilingwijzer"
