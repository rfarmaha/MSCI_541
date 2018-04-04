"""
File: search.py
Author: Ramandeep Farmaha 20516974
Date Last Modified: April 2nd, 2018
Python Version: 3.4

Submits query to document engine that performs BM25 retrieval and displays top 10 ranked results to the user
"""
import argparse
import bm25
import getDocument
import queryBiasedSummary
import pickle
import time

DIRECTORY_PATH = "../documents_w_metadata/"
TOKEN_ID_TOKEN_PATH = 'token_id_token.p'
TOKEN_TOKEN_ID_PATH = 'token_token_id.p'
TOKEN_ID_POSTINGS_PATH = 'token_id_postings.p'
DOC_NO_METADATA_PATH = '/doc_no_metadata.p'
DOC_ID_NO_PATH = '/doc_id_no.p'
TOPICS_PATH = '../topics.p'
RESULTS_PATH = 'bm25-results/'


# Import relevant dicts of tokens to postings
print("Importing relevant dicts")
token_id_postings = pickle.load(open(DIRECTORY_PATH + TOKEN_ID_POSTINGS_PATH, 'rb'))
token_id_token = pickle.load(open(DIRECTORY_PATH + TOKEN_ID_TOKEN_PATH, 'rb'))
token_token_id = pickle.load(open(DIRECTORY_PATH + TOKEN_TOKEN_ID_PATH, 'rb'))
doc_id_no = pickle.load(open(DIRECTORY_PATH + DOC_ID_NO_PATH, 'rb'))
doc_no_metadata = pickle.load(open(DIRECTORY_PATH + DOC_NO_METADATA_PATH, 'rb'))
print("Completed import")

# Calculate average doc length in collection
print("Calculating average length of documents")
average_length = sum([doc_no_metadata[doc_no].length for doc_id, doc_no in doc_id_no.items()]) / len(doc_id_no)

query = input("Enter a query: ")
start = time.time()

o_dict = bm25.calculate_bm25(0, query, token_token_id, token_id_postings, doc_id_no, doc_no_metadata, average_length, False, DIRECTORY_PATH)
# Display top ten results
limit = min(len(o_dict), 10)
i = 1
for doc_no, score in o_dict.items():
    document = doc_no_metadata[doc_no]
    print("{}. {} ({})".format(i, document.headline.replace('\n', ''), document.date))
    print(document.text)
    summary = queryBiasedSummary.summarize(query, document.text)
    print("{} ({})".format(summary, doc_no))
    break
    i += 1
    if i > limit:
        break

stop = time.time()
print(stop - start)
