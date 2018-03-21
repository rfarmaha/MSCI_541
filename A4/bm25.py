import getDocument
import math
import os
import pickle
import re

from collections import OrderedDict

TOKEN_ID_TOKEN_PATH = '/token_id_token.p'
TOKEN_TOKEN_ID_PATH = '/token_token_id.p'
TOKEN_ID_POSTINGS_PATH = '/token_id_postings.p'
DOC_ID_NO_PATH = '/doc_id_no.p'
DOCUMENTS_PATH = '../documents'
TOPICS_PATH = '../topics.p'
RESULTS_PATH = 'bm25-results/'
BASELINE = 'rfarmaha-hw4-bm25-baseline.txt'

# BM25 constants
K1 = 1.2
B = 0.75
K2 = 7


def calculate_bm25(topic_id, topic, token_token_id, postings_list, doc_id_no, average_doc_length):
    """Calculates BM25 for a topic against all LATimes Documents, returns ordered dictionary of doc_no to ranking"""
    query_tokens = tokenize(topic)
    doc_no_score = {}
    N = len(doc_id_no)

    # Calculate tf in query, and idf
    for token in query_tokens:
        qf = query_tokens.count(token)
        token_tf = ((K2 + 1)*qf) / (K2 + qf)

        # Calculate idf
        postings = postings_list[token_token_id[token]]
        # Postings follow format: [doc_id, count]
        n_i = len(postings[::2])
        a = (N - n_i + 0.5) / (n_i + 0.5)
        token_idf = math.log(a)

        # Calculate tf for docs
        for i, doc_id in enumerate(postings[::2]):
            doc_no = doc_id_no[doc_id]
            document = getDocument.retrieve_by_docno(DOCUMENTS_PATH, doc_no)

            fi = postings[i+1]
            K = K1 * ((1 - B) + B * (document.length / average_doc_length))
            doc_tf = ((K1 + 1)*fi) / (K + fi)
            score = doc_tf * token_tf * token_idf
            if doc_no in doc_no_score:
                doc_no_score[doc_no] = doc_no_score[doc_no] + score
            else:
                doc_no_score[doc_no] = score
    sorted_doc_no_score = OrderedDict(sorted(doc_no_score.items(), key=lambda t: t[1], reverse=True))

    print("Calculated scores for query: {}".format(topic_id))
    return sorted_doc_no_score


def tokenize(query):
    """Tokenizes query, copied over from indexEngine.py and modified to support query rather than document"""
    tokens = []
    # Lowercase and split on non-alphanumerics
    text = query.lower()
    text_tokens = re.split('[\W]', text)
    tokens += text_tokens

    # Remove empty strings in resulting tokens list
    tokens = list(filter(None, tokens))
    return tokens


# Create results folder
if not os.path.exists(RESULTS_PATH):
    os.makedirs(RESULTS_PATH)

# Retrieve list of topics
topics = pickle.load(open(TOPICS_PATH, 'rb'))


# Import relevant dicts of tokens to postings
print("Importing relevant dicts")
token_id_postings = pickle.load(open(DOCUMENTS_PATH + TOKEN_ID_POSTINGS_PATH, 'rb'))
token_id_token = pickle.load(open(DOCUMENTS_PATH + TOKEN_ID_TOKEN_PATH, 'rb'))
token_token_id = pickle.load(open(DOCUMENTS_PATH + TOKEN_TOKEN_ID_PATH, 'rb'))
doc_id_no = pickle.load(open(DOCUMENTS_PATH + DOC_ID_NO_PATH, 'rb'))
print("Completed import")

# Calculate average doc length in collection TODO: Remove static value
print("Calculating average length of documents")
# average_length = sum([getDocument.retrieve_by_docno(DOCUMENTS_PATH, doc_no).length for doc_id, doc_no in doc_id_no.items()]) / len(doc_id_no)
average_length = 524.3251273730818

print(average_length)

with open(RESULTS_PATH + BASELINE, 'w') as file:
    for topic_id, topic in topics.items():
        o_dict = calculate_bm25(topic_id, topic, token_token_id, token_id_postings, doc_id_no, average_length)

        # Input top 1000 documents along with their scores into results file
        limit = min(len(o_dict), 1000)
        i = 1
        for doc_no, score in o_dict.items():
            file.write("{} Q0 {} {} {} rfarmaha_bm25_baseline\n".format(topic_id, doc_no, i, score))
            i += 1
            if i > 1000:
                break