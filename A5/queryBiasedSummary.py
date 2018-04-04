"""
File: queryBiasedSummary.py
Author: Ramandeep Farmaha 20516974
Date Last Modified: April 2nd, 2018
Python Version: 3.4

Performs a query-biased summary for a given text input
"""
import re
import bm25
import heapq

STOPS = re.compile('(?<=[.!?])[ \'\"]+')
ESCAPES = re.compile(r'[\n\\]+')


class QueryBiasedSentence:
    def __init__(self, text, score):
        self.text = text
        self.score = score

    def __lt__(self, other):
        # Use the negation to trick the min heap into sorting the highest score first
        return self.score > other.score


def summarize(query, text):
    # Clean text of escaped characters
    text = re.sub(ESCAPES, '', text)
    sentences = re.split(STOPS, text)
    # Remove any sentences with less than 5 words
    trimmed_sentences = [s for s in sentences if len(s.split()) > 4]
    qb_sentences = []
    for i, sentence in enumerate(trimmed_sentences):
        tokens = bm25.tokenize(sentence)
        query_tokens = bm25.tokenize(query)
        # Let l be 2 if S is the first sentence, 1 if it is the second, 0 otherwise
        l = 0
        # Let c be the number of w_i that are query terms; including repetitions
        c = 0
        # Let d be the number of distinct query terms that match some w_i
        d = 0
        # Identify the longest contiguous run of query terms in S, say w_j …. W_j+k
        k = 0
        k_max = 0
        contiguous = False

        if i == 0:
            l = 2
        elif i == 1:
            l = 1
        for q in query_tokens:
            c += tokens.count(q)
            if q in tokens:
                d += 1
        for t in tokens:
            if t in query_tokens:
                if contiguous:
                    k += 1
                else:
                    contiguous = True
                    k = 1
                k_max = max(k, k_max)
            else:
                contiguous = False
        score = c + d + k + l
        heapq.heappush(qb_sentences, QueryBiasedSentence(sentence, score))

    while qb_sentences:
        sent = heapq.heappop(qb_sentences)
        print(sent.score, sent.text)


