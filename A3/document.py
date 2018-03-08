class Document:
    """Data wrapper object that contains raw document and metadata"""

    def __init__(self):
        self.doc_id = 0
        self.docno = ""
        self.date = ""
        self.headline = ""
        self.raw_document = ""
        self.graphic = ""
        self.text = ""
        self.length = 0
