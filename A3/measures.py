from collections import OrderedDict
import math

class Measures:
    def __init__(self, qrel, global_id, results):
        self.results = results
        self.qrel = qrel
        self.global_id = global_id

    def get_average_precision(self):
        avg_precision = {}

        for query_id in self.qrel.get_query_ids():
            relevant = 0
            precision_scores = []

            result = self.results.get_result(query_id)
            # Sort results by score
            result.sort(key=lambda t: t.score, reverse=True)

            for i, r in enumerate(result, start=1):
                if self.qrel.get_relevance(query_id, r.doc_id) > 0:
                    relevant += 1
                    precision_scores.append(float(relevant/i))

            avg_precision[query_id] = sum(precision_scores)/float(len(self.qrel.query_2_reldoc_nos[query_id]))

        avg_precision = OrderedDict(sorted(avg_precision.items(), key=lambda t: t[0]))
        return avg_precision

    def get_precision_at_10(self):
        precision_at_10 = {}

        for query_id in self.qrel.get_query_ids():
            relevant = 0

            result = self.results.get_result(query_id)
            # Sort results by score
            result.sort(key=lambda t: t.score, reverse=True)

            # Retrieve only the top ten precisions
            for r in result[:10]:
                if self.qrel.get_relevance(query_id, r.doc_id) > 0:
                    relevant += 1

            precision_at_10[query_id] = float(relevant/10)

        precision_at_10 = OrderedDict(sorted(precision_at_10.items(), key=lambda t: t[0]))
        return precision_at_10

    def get_ndcg_10_1000(self):
        """Calculates NDCG@10 and NDCG@1000"""

        ndcg_10 = {}
        ndcg_1000 = {}

        for query_id in self.qrel.get_query_ids():
            dcg = 0
            relevant_docs = len(self.qrel.query_2_reldoc_nos[query_id])

            result = self.results.get_result(query_id)
            # Sort results by score
            result.sort(key=lambda t: t.score, reverse=True)

            # Retrieve only the top ten precisions and compute dcg

            for i, r in enumerate(result, start=1):
                if self.qrel.get_relevance(query_id, r.doc_id) > 0:
                    dcg += (1/math.log2(i+1))
                if i == 10:
                    # Compute IDCG@10
                    idcg_10 = self.__get_idcg(relevant_docs, i)
                    ndcg_10[query_id] = dcg/idcg_10

                # Results may sometimes be truncated to less than 1000, in that case use the last result
                if i == min(len(result), 1000):
                    idcg_1000 = self.__get_idcg(relevant_docs, i)
                    ndcg_1000[query_id] = dcg / idcg_1000

        ndcg_10 = OrderedDict(sorted(ndcg_10.items(), key=lambda t: t[0]))
        ndcg_1000 = OrderedDict(sorted(ndcg_1000.items(), key=lambda t: t[0]))
        return ndcg_10, ndcg_1000

    def __get_idcg(self, relevant_docs, max_bound):
        idcg = 0
        if relevant_docs > 0:
            for i in range(1, min(max_bound + 1, relevant_docs + 1)):
                idcg += (1 / math.log2(i + 1))
            return idcg
        else:
            return 1
