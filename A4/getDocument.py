#!/usr/bin/env python
"""
File: getDoc.py
Author: Ramandeep Farmaha 20516974
Date Last Modified: January 22nd, 2018
Python Version: 3.4

Retrieves documents from LA Times dataset given index and either DOCNO or internal ID. For University of Waterloo course
MSCI 541.
"""

import pickle

DOCNO = 'docno'
IDX_PATH = '/doc_id_no.p'


def retrieve_by_docno(path, param):
    """Retrieve document and associated metadata from DOCNO"""
    params = param.split("-")
    # Document with DOCNO LA%MM%DD%YY-NNNN is stored in path/YY/MM/DD/NNNN.p
    file_path = "/{}/{}/{}/{}.p".format(params[0][-2:], params[0][-6:-4], params[0][-4:-2], params[1])
    file_path = path + file_path
    with open(file_path, 'rb') as f:
        document = pickle.load(f)
        return document


def retrieve_by_id(path, param):
    """Retrieve document and associated metadata from internal ID"""
    with open(path + IDX_PATH, 'rb') as file:
        doc_id_no = pickle.load(file)
        docno = doc_id_no[int(param)]
        return retrieve_by_docno(path, docno)