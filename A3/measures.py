from collections import OrderedDict


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
            for r in result[:9]:
                if self.qrel.get_relevance(query_id, r.doc_id) > 0:
                    relevant += 1

            precision_at_10[query_id] = float(relevant/10)

        precision_at_10 = OrderedDict(sorted(precision_at_10.items(), key=lambda t: t[0]))
        return precision_at_10

    def get_ndcg_10(self):
        ndcg_10 = {}



        ndcg_10 = OrderedDict(sorted(precision_at_10.items(), key=lambda t: t[0]))
        print(ndcg_10)
        return ndcg_10