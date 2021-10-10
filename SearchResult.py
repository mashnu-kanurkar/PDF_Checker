class SearchResult(dict):

    def __init__(self, text = '', font = '', size = '', color = '', bbox = ''):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.bbox = bbox

    def get_search_result(self):
        return {'text': self.text, 'font': self.font, 'size': self.size, 'color': self.color, 'bbox': self.bbox}


    def __str__(self):
        return {'text': self.text, 'font': self.font, 'size': self.size, 'color': self.color, 'bbox': self.bbox}.__str__()

