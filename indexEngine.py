import argparse
import gzip
import os.path
import pickle
import re
import time

from document import Document

DOC_OPEN_TAG = "<DOC>"
DOC_CLOSE_TAG = "</DOC>"
DOC_NO_TAG = "<DOCNO>"
HEADLINE_TAG = "<HEADLINE>"
IDX_PATH = '/doc_id_no.p'


def parse_args():
    parser = argparse.ArgumentParser(description='Retrieve documents and their associated metadata for the LA Times '
                                                 'gzip archive')
    parser.add_argument('gzip', metavar='GZIP_FILE', help='Path of LA Times .gzip file')
    parser.add_argument('directory', metavar='DOCUMENT_DIRECTORY', help='Directory to save documents and metadata')
    args = parser.parse_args()
    return args.gzip, args.directory


gzip_path, directory_path = parse_args()

# Create the directory if it doesn't exist, else throw an error
# TODO: remove exist_ok
os.makedirs(directory_path, exist_ok=True)

doc_id_no = {}

with gzip.open(gzip_path, mode='rt') as gzip_file:
    document = None
    raw_document = []
    doc_id = 0
    headline = -1

    for line in gzip_file:
        raw_document.append(line)

        # Add headline if applicable
        if headline > 0:
            headline -= 1
        elif headline == 0:
            r_line = line.rstrip()
            if r_line[-1:] == ';':
                r_line = r_line[:-1]
            document.headline = r_line
            headline = -1

        if DOC_OPEN_TAG in line:
            # Create a Document object
            document = Document()
        elif DOC_NO_TAG in line:
            # Generate document internal id
            docno = re.search('LA\d{6}-\d{4}', line).group()
            docno_list = docno.split('-')
            date = docno_list[0][2:]
            doc_id += 1
            document.doc_id = doc_id
            document.docno = docno

            # Generate formatted date
            date_obj = time.strptime(date, '%m%d%y')
            formatted_date = time.strftime('%B %d, %Y', date_obj)
            document.date = formatted_date

        elif HEADLINE_TAG in line:
            headline = 1

        elif DOC_CLOSE_TAG in line:
            raw_document_string = "".join(raw_document)
            document.raw_document = raw_document_string

            # Insert into directory YY/MM/DD
            date_obj = time.strptime(document.date, '%B %d, %Y')
            formatted_date = time.strftime('/%y/%m/%d/', date_obj)
            file_path = directory_path + formatted_date
            os.makedirs(file_path, exist_ok=True)
            file_path += document.docno.split('-')[1]
            file_path += '.p'
            doc_id_no[doc_id] = document.docno
            with open(file_path, "wb") as text_file:
                pickle.dump(document, text_file)
            print("Processed Document: {}".format(doc_id))
            # clear the raw document list
            raw_document.clear()


doc_id_no_path = directory_path + IDX_PATH
pickle.dump(doc_id_no, open(doc_id_no_path, 'wb'))

