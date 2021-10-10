import fitz
from CustomExceptions import *

class ParsePDFUsingSearchFor:
    def __init__(self, path_to_pdf, check_parameters):
        self.path_to_pdf = path_to_pdf
        self.doc = fitz.open(self.path_to_pdf)
        self.check_parameters = check_parameters
        if self.validate_pdf(self.doc):
            self.page = self.doc[0]
        else:
            raise PDFPageCountException()

    def validate_pdf(self, doc):
        try:
            if len(doc) == 1:
                return True
            else:
                return False
        except Exception as e:
            raise e

    def search_for_text(self, page, check_parameter):
        for key in check_parameter:
            page.search_for(check_parameter['text'], clip = check_parameter['bbox'])