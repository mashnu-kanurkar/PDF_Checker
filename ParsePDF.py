import fitz
from CustomExceptions import *
from SearchResult import SearchResult


class ParsePDF:
    def __init__(self, path_to_pdf):
        self.path_to_pdf = path_to_pdf
        self.doc = fitz.open(self.path_to_pdf)
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

    def find_text_within_box(self, bbox):
        try:
            parsed_data = {}
            for key in bbox:
                data_for_key = self.find_text(key, bbox)
                parsed_data[key] = data_for_key
                #print('parsed_data: ', parsed_data)
                if key == 'wef':
                    if parsed_data[key][0]['text'] == '':
                        parsed_data['has_wef'] = False
                    else:
                        parsed_data['has_wef'] = True
                elif key == 'proc_criteria':
                    if parsed_data[key][0]['text'] == '':
                        parsed_data['has_proc_criteria'] = False
                    else:
                        parsed_data['has_proc_criteria'] = True
                elif key == 'copyright':
                    if '©' not in parsed_data[key][0]['text']:
                        parsed_data[key][0]['text'] = '© {}'.format(parsed_data[key][0]['text'])

            return parsed_data
        except Exception as e:
            print(e)
            raise e

    def find_text(self, key, bbox):
        data = self.page.get_text('dict', clip=bbox[key])
        search_result_list = []
        for block in data['blocks']:
            if block['type'] == 0 and block['bbox'] != (0, 0, 0, 0):
                for line in block['lines']:
                    if line['bbox'] != (0,0,0,0):
                        for span in line['spans']:
                            text = span['text']
                            bbox = span['bbox']
                            size = span['size']
                            color = span['color']
                            font = span['font']
                            search_result = {'text': text, 'font': font, 'size': size, 'color': color, 'bbox': bbox}
                            search_result_list.append(search_result)
        if len(search_result_list) == 0:
            search_result_list = [{'text': '', 'font': '', 'size': 0, 'color': 0, 'bbox': bbox[key]}]

        return search_result_list
