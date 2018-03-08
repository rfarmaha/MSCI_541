"""
File: evaluate.py
Author: Ramandeep Farmaha 20516974
Date Last Modified: March 6th, 2018
Python Version: 3.4

Calculates several different information retrieval evaluation measures for given results and qrel files. For University
of Waterloo course MSCI 541.
"""

import argparse
import csv
import os.path
from parsers import QrelsParser, ResultsParser
from measures import Measures

BAD_FORMAT_STRING = 'bad format'

def parse_args():
    parser = argparse.ArgumentParser(description='Program that calculates Average Precision, Precision@10, NDCG@10, '
                                                 'NDCG@1000 and Time-Based Gain for a given topic results file and '
                                                 'Qrels file')
    parser.add_argument('--qrel', required=True, help='Path to qrel file')
    parser.add_argument('--results', required=True, help='Path to directory containing results files')
    args = parser.parse_args()
    return args.qrel, args.results


def measures_to_csv(name, measures):
    """Converts measure ordered dicts to CSVs"""
    if not os.path.exists('results/'):
        os.makedirs('results')
    with open('results/{}.csv'.format(name), 'w') as csvfile:
        fieldnames = ['measure', 'query_id', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for measure_key, measure in measures.measures_dict.items():
            for key, value in measure.items():
                writer.writeheader()
                writer.writerow({'measure': measure_key, 'query_id': key, 'score': value})


def append_to_average_file(name, measures):
    """Adds measures for a specific run to averages file"""
    with open('results/average_measures.csv', 'a') as csvfile:
        fieldnames = ['Run Name', 'Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@1000', 'Mean TBG']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        mean_ap = get_average_from_measure(measures.average_precision)
        mean_p_10 = get_average_from_measure(measures.precision_at_10)
        mean_ndcg_10 = get_average_from_measure(measures.ndcg_10)
        mean_ndcg_1000 = get_average_from_measure(measures.ndcg_1000)
        mean_tbg = get_average_from_measure(measures.time_based_gain)
        writer.writerow({'Run Name': name,
                         'Mean Average Precision': '{:.3f}'.format(mean_ap),
                         'Mean P@10': '{:.3f}'.format(mean_p_10),
                         'Mean NDCG@10': '{:.3f}'.format(mean_ndcg_10),
                         'Mean NDCG@1000': '{:.3f}'.format(mean_ndcg_1000),
                         'Mean TBG': '{:.3f}'.format(mean_tbg)})


def get_average_from_measure(measure):
    return float(sum(measure.values())) / len(measure.values())


def bad_format_run(name):
    with open('results/average_measures.csv', 'a') as csvfile:
        fieldnames = ['Run Name', 'Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@1000', 'Mean TBG']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Run Name': name,
                         'Mean Average Precision': BAD_FORMAT_STRING,
                         'Mean P@10': BAD_FORMAT_STRING,
                         'Mean NDCG@10': BAD_FORMAT_STRING,
                         'Mean NDCG@1000': BAD_FORMAT_STRING,
                         'Mean TBG': BAD_FORMAT_STRING})


qrel_path, results_dir_path = parse_args()
qrel = QrelsParser(qrel_path).parse()
results_files = os.listdir(results_dir_path)

if not os.path.exists('results/'):
    os.makedirs('results')
with open('results/average_measures.csv', 'w') as csvfile:
    fieldnames = ['Run Name', 'Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@1000', 'Mean TBG']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

results_measures = []

for r in results_files:
    name = r.split(".")[0]
    if "student" in name:
        print("Computing measures for: {}".format(name))
        try:
            results = ResultsParser(results_dir_path + r).parse()
            measures = Measures(qrel, results[0], results[1])
            measures_to_csv(name, measures)
            append_to_average_file(name, measures)
        except (ResultsParser.ResultsParseError, ValueError, FileNotFoundError) as e:
            print(e)
            bad_format_run(name)
            continue
