import pandas as pd
import os
import csv
import time
from mining import apriori, generate_association_rules, brute_force


def load_trans_db():
    filenames = next(os.walk('transactions'), (None, None, []))[2]
    for file in filenames:
        transactions = {}
        with open(f'transactions/{file}', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.setdefault(row['id'], []).append(row['transaction'])
        yield transactions


def pretty_print_rules(association_rules):
    for x, y, support, confidence  in association_rules:
        print(f'    {x} -> {y}: Support {support}%, Confidence {confidence}%')


if __name__ == '__main__':
    print("Hello and welcome to association rule miner!")
    print("please specify the minimum support level you would like to use.")
    support_level = input("Minimum support level:")
    support_level = int(support_level)
    print("great thanks! what is the minimum confidence level you would like?")
    confidence_level = input("Minimum Confidence level:")
    confidence_level = int(confidence_level)
    print()
    print('Generating association rules...')
    print()
    current = 1
    for db in load_trans_db():
        print(f'For transaction database {current} we got the following results')
        trans_set_list = [set(x) for x in db.values()]
        a_start = time.time()
        a_rules = apriori(trans_set_list, support_level)
        a_end = time.time()
        a_exe_time = round(a_end - a_start, 5)
        b_start = time.time()
        b_rules = brute_force(trans_set_list, support_level)
        b_end = time.time()
        b_exe_time = round(b_end - b_start,5)
        a_assoc_rules = generate_association_rules(a_rules, confidence_level, len(trans_set_list))
        b_assoc_rules = generate_association_rules(b_rules, confidence_level, len(trans_set_list))
        print('Association Rule results using apriori algorithm:')
        print(f'execution time is {a_exe_time} seconds')
        pretty_print_rules(a_assoc_rules)
        print()
        print('Association Rules results using brute force algorithm')
        print(f'execution time is {b_exe_time} seconds')
        pretty_print_rules(b_assoc_rules)
        print()
        current = current + 1
