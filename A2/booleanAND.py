import argparse
import os
import pickle
import re

DOC_ID_NO_PATH = '/doc_id_no.p'
TOKEN_ID_TOKEN_PATH = '/token_id_token.p'
TOKEN_TOKEN_ID_PATH = '/token_token_id.p'
TOKEN_ID_POSTINGS_PATH = '/token_id_postings.p'


def parse_args():
    parser = argparse.ArgumentParser(description='Perform boolean AND retrieval for a list of queries')
    parser.add_argument('index', metavar='INDEX', help='Path to LATimes inverted index directory')
    parser.add_argument('queries', metavar='QUERIES', help='Path to queries pickle file')
    parser.add_argument('output', metavar='OUTPUT_FILE', help='Path to output results text file')
    args = parser.parse_args()
    return args.index, args.queries, args.output


def tokenize(query):
    query = query.lower()
    tokens = re.split('[\W]', query)

    # Remove empty strings in resulting tokens list
    tokens = list(filter(None, tokens))
    return tokens


index, queries, output = parse_args()

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
with open(index + TOKEN_TOKEN_ID_PATH, 'rb') as t_d:
    token_to_token_id = pickle.load(t_d)

# Load the token_to_token_id dict
with open(index + TOKEN_ID_POSTINGS_PATH, 'rb') as t_p:
    token_id_to_postings = pickle.load(t_p)

# Load the token_to_token_id dict
with open(index + DOC_ID_NO_PATH, 'rb') as t_id:
    doc_id_no = pickle.load(t_id)

# Remove the output file if it already exists
try:
    os.remove(output)
except OSError:
    pass

with open(output, 'w') as o:
    for number, query in query_dict.items():
        tokens = tokenize(query)
        result_set = set()

        for t in tokens:
            token_id = token_to_token_id[t]
            postings_list = token_id_to_postings[token_id]
            # Postings list uses following schema: [doc_id, token_count] i.e. every even entry is doc_id, odd is token_count
            if result_set:
                result_set = result_set.intersection(postings_list[::2])
            else:
                result_set = result_set.union(set(postings_list[::2]))

        doc_no_rank_list = [(i, doc_id_no[doc_id]) for i, doc_id in enumerate(result_set, start=1)]

        doc_list_length = len(doc_no_rank_list)
        for i, doc_no in doc_no_rank_list:
            score = doc_list_length - i
            o.write("{} q0 {} {} {} rfarmahaAND\n".format(number, doc_no, i, score))
