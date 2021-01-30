import pickle
from collections import namedtuple


Peiling = namedtuple('Peiling', ['verwacht', 'laag', 'hoog'])

with open('peilingen.pkl', 'rb') as fh:
    numbers = pickle.load(fh)
with open('table.pkl', 'rb') as fh:
    table = pickle.load(fh)

parties = list(numbers.keys())

print(numbers)
print([table[(party,)] for party in parties])
