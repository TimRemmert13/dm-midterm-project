from items import items
from random import randint
import pandas as pd


def build_transactions_db(max_trans_size):
    for k in range(0, 5):
        trans_column = []
        for i in range(0, 20):
            trans_size = randint(1, max_trans_size)
            trans_list = []
            for t in range(0, trans_size):
                trans_list.append(get_item())
            trans_column.append({'transaction': trans_list})
        trans_db = pd.DataFrame(trans_column)
        trans_db = trans_db.explode('transaction').reset_index()
        trans_db.columns = ['id', 'transaction']
        trans_db.to_csv(f'transactions/trans_db_{k}.csv', index=False)


def get_item():
    idx = randint(0, len(items) - 1)
    return items[idx]
