import pandas as pd
from collections import namedtuple
import pickle

numbers = pd.read_excel('Cijfers_Peilingwijzer.xlsx', header=0, index_col=0)

partijen = numbers.index.values
expected = numbers.Zetels.values
low = numbers.ZetelsLaag.values
high = numbers.ZetelsHoog.values

Peiling = namedtuple('Peiling', ['verwacht', 'laag', 'hoog'])

peilingen = {partij: Peiling(*x) for partij, *x in zip(partijen, expected, low, high)}

print(peilingen)

with open('peilingen.pkl', 'wb') as fh:
    pickle.dump(peilingen, fh)
