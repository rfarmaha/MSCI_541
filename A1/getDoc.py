#!/usr/bin/env python
"""
File: getDoc.py
Author: Ramandeep Farmaha 20516974
Date Last Modified: January 22nd, 2018
Python Version: 3.4

Retrieves documents from LA Times dataset given index and either DOCNO or internal ID. For University of Waterloo course
MSCI 541.
"""

import argparse
import pickle

DOCNO = 'docno'
IDX_PATH = '/doc_id_no.p'


def parse_args():
    parser = argparse.ArgumentParser(description='Retrieves document from index given either DOCNO or internal ID')
    parser.add_argument('directory', metavar='DOCUMENT_DIRECTORY', help='Directory of indexed documents and metadata')
    parser.add_argument('is_docno', metavar='DOC_NO OR ID', help='Either \'docno\' to search by DOCNO or \'id\' '
                                                                 'to search by ID')
    parser.add_argument('search_param', metavar='SEARCH_PARAMETER', help='The DOCNO or ID to be searched')
    args = parser.parse_args()
    return args.directory, args.is_docno == 'docno', args.search_param


def retrieve_by_docno(path, param):
    """Retrieve document and associated metadata from DOCNO"""
    params = param.split("-")
    # Document with DOCNO LA%DD%MM%YY-NNNN is stored in path/YY/MM/DD/NNNN.p
    file_path = "/{}/{}/{}/{}.p".format(params[0][-2:], params[0][-4:-2], params[0][-6:-4], params[1])
    file_path = path + file_path
    with open(file_path, 'rb') as f:
        document = pickle.load(f)
        print("docno: {}\ninternal id: {}\ndate: {}\nheadline: {}\nraw document:\n{}"
              .format(document.docno, document.doc_id, document.date, document.headline, document.raw_document))


def retrieve_by_id(path, param):
    """Retrieve documetn and associated metadata from internal ID"""
    with open(path + IDX_PATH, 'rb') as file:
        doc_id_no = pickle.load(file)
        docno = doc_id_no[int(param)]
        return retrieve_by_docno(path, docno)


gzip_path, is_docno, search_param = parse_args()

if is_docno:
    retrieve_by_docno(gzip_path, search_param)
else:
    retrieve_by_id(gzip_path, search_param)