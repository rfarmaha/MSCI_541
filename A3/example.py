import argparse
import sys
from parsers import QrelsParser, ResultsParser

# Author: Nimesh Ghelani based on code by Mark D. Smucker

parser = argparse.ArgumentParser(description='todo: insert description')
parser.add_argument('--qrel', required=True, help='Path to qrel')
parser.add_argument('--results', required=True, help='Path to file containing results')
parser.add_argument('--max-results', type=int, required=False, help='')

# This code doesn't do much other than sort of show how the 
# various classes can be used.

def main():
    cli = parser.parse_args()
    qrel = QrelsParser(cli.qrel).parse()
    results = ResultsParser(cli.results).parse()
    max_results = cli.max_results

    query_ids = sorted(qrel.get_query_ids())

    for query_id in query_ids:
        query_result = sorted(results[1].get_result(query_id))
        if query_result is None:
            sys.stderr.write(query_id+' has no results, but it exists in the qrels.\n')
            continue

        for result in query_result[:max_results]:
            relevance = qrel.get_relevance(query_id, result.doc_id)
            # okay, would need to do more here..


if __name__ == '__main__':
    main()
