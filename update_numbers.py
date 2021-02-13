from collections import namedtuple
import pickle
import statistics
import math
import itertools
import json

from tqdm import tqdm
import pandas as pd

# polls
numbers_url = "https://d1bjgq97if6urz.cloudfront.net/Public/Peilingwijzer/Last/Cijfers_Peilingwijzer.xlsx"
# numbers_url = "Cijfers_Peilingwijzer.xlsx"
numbers = pd.read_excel(numbers_url, header=0, index_col=0)

if numbers.empty:
    raise SystemExit("Loading Excel file gives empty dataframe, for some reason.")

with open('last_updated.json', 'r') as fh:
    last_update = json.load(fh)

# check if Peilingwijzer numbers actually changed since last update
numbers_were_changed = numbers.Datum.max() > pd.Timestamp(last_update["data"])
if not numbers_were_changed:
    raise SystemExit("No updates on the Peilingwijzer numbers, done!")


partijen = numbers.index.values
expected = numbers.Zetels.values
low = numbers.ZetelsLaag.values
high = numbers.ZetelsHoog.values

Peiling = namedtuple('Peiling', ['verwacht', 'laag', 'hoog'])

peilingen = {partij: Peiling(int(e), int(l), int(h)) for partij, e, l, h in zip(partijen, expected, low, high)}

print(peilingen)

with open('peilingen.pkl', 'wb') as fh:
    pickle.dump(peilingen, fh)

# simulations

sims_df = pd.read_csv("https://d1bjgq97if6urz.cloudfront.net/Public/Peilingwijzer/Last/coa_seats.csv",
                      index_col=0, header=0)

sims = {party: tuple(sims_df[party]) for party in sims_df}

# preprocess simulations into combinations table for 1000x faster retrieval in webapp

def sum_coalition(data, *parties):
    result = sum(data[party] for party in parties)
    if isinstance(result, int) and result == 0:
        return pd.Series([], dtype='int')
    else:
        return result

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def to_Peiling_from_simulations(simulations):
    def estimate_Peiling(est, std):
        interval = math.ceil((2 * std))
        return Peiling(verwacht=int(est),
                       laag=int(max(0, est - interval)),
                       hoog=int(min(est + interval, 150)))

    if len(simulations) == 0:
        return Peiling(0, 0, 0)
    est = round(statistics.mean(simulations))
    return estimate_Peiling(est, statistics.stdev(simulations))

table = {}
for key in tqdm(powerset(sims.keys()), total=2**len(sims.keys())):
    table[key] = to_Peiling_from_simulations(sum_coalition(sims_df, *key))

# make sure the simulations were also updated and so they should
# not contain the same answers as the previous table:
with open('table.pkl', 'rb') as fh:
    old_table = pickle.load(fh)

if table == old_table:
    raise SystemExit("The new table is exactly the same as the old one, so probably it wasn't updated yet, try again later!")

# everything fine, save stuff to files
with open('table.pkl', 'wb') as fh:
    pickle.dump(table, fh)

last_update["data"] = numbers.Datum.max().date().__str__()
last_update["page"] = pd.Timestamp.now('Europe/Amsterdam').date().__str__()
print(last_update)
with open('last_updated.json', 'w') as outfile:
    json.dump(last_update, outfile)
