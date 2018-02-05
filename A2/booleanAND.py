import argparse
import os
import pickle
import re

import indexEngine


def parse_args():
    parser = argparse.ArgumentParser(description='Perform boolean AND retrieval for a list of queries')
    parser.add_argument('index', metavar='INDEX', help='Path to LATimes inverted index directory')
    parser.add_argument('queries', metavar='QUERIES', help='Path to queries pickle file')
    parser.add_argument('results', metavar='RESULTS', help='Path to output results text file')
    args = parser.parse_args()
    return args.index, args.queries, args.results


def tokenize(query):
    tokens = []
    query = query.lower()
    tokens = re.split('[\W]', query)

    # Remove empty strings in resulting tokens list
    tokens = list(filter(None, tokens))
    return tokens

index, queries, results = parse_args()

# Check if index exists
if not os.path.exists(index):
    print("Index file doesn't exist in the specified location! Please correct this issue.")
    exit(1)

# Check if queries file exists
if not os.path.exists(queries):
    print("Index file doesn't exist in the specified location! Please correct this issue.")
    exit(1)

# Load the queries from the query file
with open(queries, 'rb') as q:
    query_dict = pickle.load(q)

# Load the token_to_token_id dict
with open(index + indexEngine.TOKEN_TOKEN_ID_PATH, 'rb') as t_d:
    token_to_token_id = pickle.load(t_d)

for number, query in query_dict.items():
    tokens = tokenize(query)

    for t in tokens:
        token_id = token_to_token_id[t]
        print(token_id)
