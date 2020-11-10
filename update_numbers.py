import pandas as pd
from collections import namedtuple
import pickle

# polls

try:
    numbers = pd.read_excel('Cijfers_Peilingwijzer.xlsx', header=0, index_col=0)
except AttributeError:
    numbers = pd.read_excel('Cijfers_Peilingwijzer.xlsx', header=0, index_col=0, engine='openpyxl')

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

with open('simulations.pkl', 'wb') as fh:
    pickle.dump(sims, fh)

