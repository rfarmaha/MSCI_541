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
import pandas as pd
from parsers import QrelsParser, ResultsParser
from scipy import stats
from measures import Measures

BAD_FORMAT_STRING = 'bad format'


def parse_args():
    parser = argparse.ArgumentParser(description='Program that calculates Average Precision, Precision@10, NDCG@10, '
                                                 'NDCG@1000 and Time-Based Gain for a given topic results file and '
                                                 'Qrels file')
    parser.add_argument('--qrel', required=True, help='Path to qrel file')
    parser.add_argument('--output_directory', required=True, help='Path to desired output directory')
    parser.add_argument('--results', required=False, help='Path to directory containing results files')
    parser.add_argument('--results_files', required=False, nargs='+', help='Space delimited list of results files')
    parser.add_argument('--compare', required=False, nargs=2, help='Outputs topics for which output_file_1 performs '
                                                                   'better than output_file_1')
    args = parser.parse_args()
    return args.qrel, args.output_directory, args.results, args.results_files, args.compare


def measures_to_csv(name, measures, output_location):
    """Converts measure ordered dicts to CSVs"""
    if not os.path.exists(output_location):
        os.makedirs(output_location[::-1])
    with open(output_location + '{}.csv'.format(name), 'w') as csvfile:
        fieldnames = ['measure', 'query_id', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for measure_key, measure in measures.measures_dict.items():
            for key, value in measure.items():
                writer.writerow({'measure': measure_key, 'query_id': key, 'score': value})


def append_to_average_file(csv_name, name, measures):
    """Adds measures for a specific run to averages file"""
    with open(csv_name, 'a') as csvfile:
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


def bad_format_run(name, output_location):
    with open(output_location + 'average_measures.csv', 'a') as csvfile:
        fieldnames = ['Run Name', 'Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@1000', 'Mean TBG']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Run Name': name,
                         'Mean Average Precision': BAD_FORMAT_STRING,
                         'Mean P@10': BAD_FORMAT_STRING,
                         'Mean NDCG@10': BAD_FORMAT_STRING,
                         'Mean NDCG@1000': BAD_FORMAT_STRING,
                         'Mean TBG': BAD_FORMAT_STRING})


def calculate_summary_statistics(output_location):
    results_dir_path = output_location
    average_csv = 'average_measures.csv'
    measures = ['Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@1000', 'Mean TBG']
    measures_dict = {'Mean Average Precision': 'average_precision',
                     'Mean P@10': 'precision_at_10',
                     'Mean NDCG@10': 'ndcg_10',
                     'Mean NDCG@1000': 'ndcg_1000',
                     'Mean TBG': 'time_based_gain'}

    if not os.path.exists(results_dir_path):
        print("Results don't exist, re-run evaluate.py")
        return

    with open(results_dir_path + 'summary_statistics.csv', 'w') as csvfile:
        fieldnames = ['Effectiveness Measure', 'Best Run Score', 'Second Best Run Score', 'Relative Percent Improvement',
                      'Two-sided Paired t-Test p-value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        df = pd.read_csv(results_dir_path + average_csv)
        # Remove any student that has no results due to bad formatting
        if "bad format" in df["Mean Average Precision"]:
            df = df.drop(df[df["Mean Average Precision"] == "bad format"].index)

        for m in measures:
            # Convert the value columns to floats to allow numeric handling
            df[m] = df[m].astype(float)
            max_score = df[m].max(axis=0)

            # Get highest scoring student run
            max_score_row = df[df[m] == max_score]
            max_score_row_name = max_score_row["Run Name"].item()

            # Get second highest scoring student run
            temp = df.drop(df[df["Run Name"] == max_score_row_name].index)
            if not temp.empty:
                max_score_2 = temp[m].max(axis=0)
                max_score_2_row = temp[temp[m] == max_score_2]
                max_score_2_name = max_score_2_row["Run Name"].item()

                max_scores = get_raw_scores(results_dir_path, max_score_row_name, measures_dict[m])
                max_2_scores = get_raw_scores(results_dir_path, max_score_2_name, measures_dict[m])

                if len(max_scores) == len(max_2_scores):
                    p_value = stats.ttest_rel(max_scores, max_2_scores)[1]
                else:
                    # Hack fix to force comparison of two unequal sets: find the means and input them each twice into
                    # a list. i.e. [avg_1, avg_1] and [avg_2, avg_2]. This prevents numpy.mean() from complaining about
                    # having only a single value in a list to compute the mean for
                    max_scores_avg = [sum(max_scores) / len(max_scores), sum(max_scores) / len(max_scores)]
                    max_2_scores_avg = [sum(max_2_scores) / len(max_2_scores), sum(max_2_scores) / len(max_2_scores)]
                    p_value = stats.ttest_rel(max_scores_avg, max_2_scores_avg)[1]

                improvement = (max_score / max_score_2 - 1)*100

                print("Summary stats for {}".format(m))
                writer.writerow({'Effectiveness Measure': m,
                                 'Best Run Score': '{:.3f}'.format(max_score),
                                 'Second Best Run Score': '{:.3f}'.format(max_score_2),
                                 'Relative Percent Improvement': '{:.3f}%'.format(improvement),
                                 'Two-sided Paired t-Test p-value': p_value})
            else:
                print("Summary stats for {}".format(m))
                print("Only a single row, possibly due to bad format")
                writer.writerow({'Effectiveness Measure': m,
                                 'Best Run Score': '{:.3f}'.format(max_score),
                                 'Second Best Run Score': 'N/A',
                                 'Relative Percent Improvement': 'N/A',
                                 'Two-sided Paired t-Test p-value': 'N/A'})


def get_raw_scores(results_dir_path, name, measure):
    """Returns raw scores for a specific measure of a given run"""
    filepath = results_dir_path + name + ".csv"
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        measures = df[df['measure'] == measure]['score']
        return measures.tolist()
    else:
        print("Results file doesn't exist for {}".format(name))


def calculate_measures(qrel, results_files, results_dir_path, output_location):
    if not os.path.exists(output_location):
        os.makedirs(output_location[:-1])
    csv_name = output_location + 'average_measures.csv'
    with open(csv_name, 'w') as csvfile:
        fieldnames = ['Run Name', 'Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@1000', 'Mean TBG']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for r in results_files:
        name = r.split(".")[0]
        print("Computing measures for: {}".format(name))
        try:
            results = ResultsParser(results_dir_path + r).parse()
            measures = Measures(qrel, results[0], results[1])
            measures_to_csv(name, measures, output_location)
            append_to_average_file(csv_name, name, measures)
        except (ResultsParser.ResultsParseError, ValueError, FileNotFoundError) as e:
            print("Cannot print: {}, bad format".format(name))
            bad_format_run(name, output_location)
            continue


def calculate_measures_results_files(qrel, results_files, output_location):
    if not os.path.exists(output_location):
        os.makedirs(output_location[:-1])
    csv_name = output_location + 'average_measures.csv'
    with open(csv_name, 'w') as csvfile:
        fieldnames = ['Run Name', 'Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@1000', 'Mean TBG']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for r in results_files:
        filename = r.split("/")
        filename = filename[len(filename) - 1]
        name = filename.split(".")[0]
        print("Computing measures for: {}".format(name))
        try:
            results = ResultsParser(r).parse()
            measures = Measures(qrel, results[0], results[1])
            measures_to_csv(name, measures, output_location)
            append_to_average_file(csv_name, name, measures)
        except (ResultsParser.ResultsParseError, ValueError, FileNotFoundError) as e:
            print("Cannot print: {}, bad format".format(name))
            bad_format_run(name, output_location)
            continue


def compare_results(output_1, output_2, output_location):
    if not os.path.exists(output_location):
        os.makedirs(output_location[:-1])
    """Outputs csv that contains all topics for which output_1 performed better than output_2 for evaluation scores"""
    df_1 = pd.read_csv(output_1)
    df_2 = pd.read_csv(output_2)
    # Only do a left join since we're looking for only where output_1 performs better
    new_df = pd.merge(df_1, df_2, how='left', left_on=['measure', 'query_id'], right_on=['measure', 'query_id'])
    new_df = new_df.drop(new_df[new_df["score_x"] <= new_df["score_y"]].index)
    new_df.sort_values(by=['query_id'], inplace=True)
    csv_name = output_location + 'compare.csv'
    new_df.to_csv(csv_name, index=False)


qrel_path, output_location, results_dir_path, results_files, compare = parse_args()
qrel = QrelsParser(qrel_path).parse()

if results_dir_path is not None:
    results_dir_files = os.listdir(results_dir_path)
    calculate_measures(qrel, results_dir_files, results_dir_path, output_location)
    calculate_summary_statistics(output_location)
elif results_files is not None:
    calculate_measures_results_files(qrel, results_files, output_location)
    calculate_summary_statistics(output_location)
    if compare is not None:
        compare_results(compare[0], compare[1], output_location)
