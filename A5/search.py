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

DIRECTORY_PATH = "../documents/"
TOKEN_ID_TOKEN_PATH = 'token_id_token.p'
TOKEN_TOKEN_ID_PATH = 'token_token_id.p'
TOKEN_ID_POSTINGS_PATH = 'token_id_postings.p'
DOC_ID_NO_PATH = '/doc_id_no.p'
TOPICS_PATH = '../topics.p'
RESULTS_PATH = 'bm25-results/'


# Import relevant dicts of tokens to postings
print("Importing relevant dicts")
token_id_postings = pickle.load(open(DIRECTORY_PATH + TOKEN_ID_POSTINGS_PATH, 'rb'))
token_id_token = pickle.load(open(DIRECTORY_PATH + TOKEN_ID_TOKEN_PATH, 'rb'))
token_token_id = pickle.load(open(DIRECTORY_PATH + TOKEN_TOKEN_ID_PATH, 'rb'))
doc_id_no = pickle.load(open(DIRECTORY_PATH + DOC_ID_NO_PATH, 'rb'))
print("Completed import")

# Calculate average doc length in collection
print("Calculating average length of documents")
#average_length = sum([getDocument.retrieve_by_docno(DIRECTORY_PATH, doc_no).length for doc_id, doc_no in doc_id_no.items()]) / len(doc_id_no)
average_length = 524.3251273730818
print(average_length)
query = input("Enter a query: ")
start = time.time()

o_dict = bm25.calculate_bm25(0, query, token_token_id, token_id_postings, doc_id_no, average_length, False, DIRECTORY_PATH)
# # Display top ten results
# limit = min(len(o_dict), 10)
# i = 1
# for doc_no, score in o_dict.items():
#     document = getDocument.retrieve_by_docno(DIRECTORY_PATH, doc_no)
#     print("{}. {} ({})".format(i, document.headline.replace('\n', ''), document.date))
#     print(document.text)
#     queryBiasedSummary.summarize(query, document.text)
#     break
#     i += 1
#     if i > limit:
#         break

stop = time.time()
print(stop - start)