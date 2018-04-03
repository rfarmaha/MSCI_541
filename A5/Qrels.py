
# Author: Nimesh Ghelani based on code by Mark D. Smucker

from collections import defaultdict
class Judgement:
    def __init__(self, query_id, doc_id, relevance):
        self.query_id = query_id
        self.doc_id = doc_id
        self.relevance = relevance

    def key(self):
        return self.query_id + '-' + self.doc_id

class Qrels:
    def QrelsError(Exception):
        pass

    def __init__(self):
        self.judgements = {}
        self.query_2_reldoc_nos = defaultdict(set)

    def add_judgement(self, j):
        if j.key() in self.judgements:
            raise QrelsError('Cannot have duplicate queryID and docID data points')

        self.judgements[j.key()] = j

        if j.relevance != 0:
            self.query_2_reldoc_nos[j.query_id].add(j.doc_id)

    def get_query_ids(self):
        return self.query_2_reldoc_nos.keys()

    def get_relevance(self, query_id, doc_id):
        key = query_id + '-' + doc_id
        if key in self.judgements:
            return self.judgements[key].relevance
        return 0
