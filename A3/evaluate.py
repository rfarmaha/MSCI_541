"""
File: evaluate.py
Author: Ramandeep Farmaha 20516974
Date Last Modified: March 6th, 2018
Python Version: 3.4

Calculates several different information retrieval evaluation measures for given results and qrel files. For University
of Waterloo course MSCI 541.
"""

import argparse
import os, os.path
from parsers import QrelsParser, ResultsParser
from measures import Measures


def parse_args():
    parser = argparse.ArgumentParser(description='Program that calculates Average Precision, Precision@10, NDCG@10, '
                                                 'NDCG@1000 and Time-Based Gain for a given topic results file and '
                                                 'Qrels file')
    parser.add_argument('--qrel', required=True, help='Path to qrel file')
    parser.add_argument('--results', required=True, help='Path to directory containing results files')
    args = parser.parse_args()
    return args.qrel, args.results


qrel_path, results_dir_path = parse_args()
qrel = QrelsParser(qrel_path).parse()
results_files = os.listdir(results_dir_path)

results_measures = []

for r in results_files:
    try:
        if r == "student1.results":
            results = ResultsParser(results_dir_path + r).parse()
            measures = Measures(qrel, results[0], results[1])
            avg_precision = measures.get_average_precision()
            precision_at_10 = measures.get_precision_at_10()
            # TODO: Remove break below
            break
    except FileNotFoundError:
        print('Error reading results file')
