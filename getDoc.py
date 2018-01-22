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


def retrieve_by_docno(gzip_path, search_param):
    params = search_param.split("-")
    file_path = "/{}/{}/{}/{}.txt".format(params[0][-2:], params[0][-4:-2], params[0][-6:-4], params[1])
    file_path = gzip_path + file_path
    with open(file_path, "rt") as text_file:
        for line in text_file:
            print(line.rstrip())


def retrieve_by_id(gzip_path, search_param):
    with open(gzip_path + IDX_PATH, 'r') as file:
        doc_id_no = pickle.load(file)
        docno = doc_id_no[search_param]
        return retrieve_by_docno(gzip_path, docno)


gzip_path, is_docno, search_param = parse_args()

if is_docno:
    retrieve_by_docno(gzip_path, search_param)
else:
    retrieve_by_id(gzip_path, search_param)