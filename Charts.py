import logger
from filename import FilenameProcessor, ManualDataProcessor, PDFPageProcessor
import os
from ParsePDF import ParsePDF
from Constants import Constants
import TextUtil
from Settings import AppConfig


class Chart():
    def __init__(self, args_dict):  # vao, wef, icao, iata, country, city, name, chart_number, is_back_page
        self.args_dict = args_dict

    def get_args_dict(self):
        try:
            return self.args_dict
        except Exception as e:
            raise e

    def add_args_key_val(self, key, value):
        try:
            self.args_dict[key] = value
        except Exception as e:
            raise e


class ReferenceChart(Chart):
    def __init__(self, pdf_path, vao='', wef='', has_wef=True, country_icao_iata='', city='', ad_name='',
                 copyright='©NAVBLUE', proc_criteria='PANS OPS', amdt_num=''):
        self.filename = os.path.splitext(os.path.basename(pdf_path))[0]
        self.filenameProcessor = FilenameProcessor(self.filename)
        self.manualDataProcessor = ManualDataProcessor(filename=self.filename, vao=vao, wef=wef, has_wef=has_wef,
                                                       country_icao_iata=country_icao_iata, city=city, ad_name=ad_name,
                                                       copyright=copyright, proc_criteria=proc_criteria,
                                                       amdt_num=amdt_num)
        super().__init__(self.get_reference_data())

    def get_reference_data(self):
        try:
            ref_data = {}
            ref_data['vao'] = [{'text': self.manualDataProcessor.get_vao(), 'font': Constants.font['vao'],
                                'size': Constants.text_size['vao']}]

            wef_date = self.manualDataProcessor.get_wef()
            ref_data['wef'] = [{'text': wef_date, 'font': '' if wef_date == '' else Constants.font['wef'],
                                'size': 0 if wef_date == '' else Constants.text_size['wef']}]
            ref_data['has_wef'] = self.manualDataProcessor.get_has_wef()
            ref_data['copyright'] = [
                {'text': self.manualDataProcessor.get_copyright(), 'font': Constants.font['copyright'],
                 'size': Constants.text_size['copyright']}]

            proc_criteria = self.manualDataProcessor.get_proc_criteria()
            ref_data['proc_criteria'] = [
                {'text': proc_criteria, 'font': '' if proc_criteria == '' else Constants.font['proc_criteria'],
                 'size': 0 if proc_criteria == '' else Constants.text_size['proc_criteria']}]
            ref_data['country_icao_iata'] = [
                {'text': self.manualDataProcessor.get_country_icao_iata(), 'font': Constants.font['country_icao_iata'],
                 'size': Constants.text_size['country_icao_iata']}]
            # index 0 for city, index 1 for ad_name
            ref_data['city'] = [{'text': self.manualDataProcessor.get_city(), 'font': Constants.font['city'],
                                 'size': Constants.text_size['city']},
                                {'text': self.manualDataProcessor.get_ad_name(), 'font': Constants.font['ad_name'],
                                 'size': Constants.text_size['ad_name']}]
            # ref_data['name'] = self.filenameProcessor.get_name()
            ref_data['chart_num_top'] = [
                {'text': self.filenameProcessor.get_chart_number(), 'font': Constants.font['chart_num_top'],
                 'size': Constants.text_size['chart_num_top']}]
            ref_data['chart_num_tab'] = [
                {'text': self.filenameProcessor.get_chart_number(), 'font': Constants.font['chart_num_tab'],
                 'size': Constants.text_size['chart_num_tab']}]
            ref_data['filename'] = [
                {'text': self.filename, 'font': Constants.font['filename'], 'size': Constants.text_size['filename']}]
            ref_data['has_proc_criteria'] = self.filenameProcessor.get_has_proc_criteria()

            amdt_num = self.manualDataProcessor.get_amdt_num()
            ref_data['amdt_num'] = [{'text': amdt_num, 'font': '' if amdt_num == '' else Constants.font['amdt_num'],
                                     'size': 0 if amdt_num == '' else Constants.text_size['amdt_num']}]
            return ref_data
        except Exception as e:
            raise e


class ChartToCheck(Chart):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.filename = os.path.basename(pdf_path)
        super().__init__(self.get_parsed_data())

    def get_parsed_data(self):
        try:
            parsePDF = ParsePDF(self.pdf_path)
            constants = Constants()
            return parsePDF.find_text_within_box(constants.get_bbox(self.pdf_path, self.filename))
        except Exception as e:
            raise e


class CompareCharts(Chart):

    def __init__(self, chart1, chart2):
        self.chart1 = chart1
        self.chart2 = chart2
        self.app_config = AppConfig()
        super().__init__(self.compare_all())


    def compare_all(self):
        comparision_dict = {}
        print('chart_1', self.chart1.get_args_dict())
        print('chart_2', self.chart2.get_args_dict())
        if not len(self.chart1.get_args_dict().keys()) == len(self.chart2.get_args_dict().keys()):
            self.chart1.add_args_key_val('country_icao_iata_left', self.chart1.get_args_dict()['country_icao_iata'])
            self.chart1.add_args_key_val('city_left', self.chart1.get_args_dict()['city'])

        for key in self.chart1.get_args_dict():
            # print('Chart 1: {} - {}'.format(key, self.chart1.get_args_dict()[key]))
            # print('Chart 2: {} - {}'.format(key, self.chart2.get_args_dict()[key]))
            try:
                logger.log(logger.INFO, 'Reference data: {} - {}'.format(key, self.chart1.get_args_dict()[key]))
                logger.log(logger.INFO, 'Parsed data: {} - {}'.format(key, self.chart2.get_args_dict()[key]))
            except Exception as e:
                raise e
            data_chart_1 = self.chart1.get_args_dict()[key]

            if type(self.chart2.get_args_dict()[key]).__name__ == 'bool':
                data_chart_2 = self.chart2.get_args_dict()[key]
            elif type(self.chart2.get_args_dict()[key]).__name__ == 'list':
                data_chart_2 = self.chart2.get_args_dict()[key]
            else:
                data_chart_2 = self.chart2.get_args_dict()[key]['text']

            if type(data_chart_1).__name__ == 'list':
                if key == 'city' or key == 'city_left':
                    city_index = 0
                    ad_name_index = 0
                    ref_name_list = [data_chart_1[0]['text'], data_chart_1[1]['text']]
                    parsed_name_list = []
                    for parsed_data in data_chart_2:
                        parsed_name = parsed_data['text'].strip()
                        if parsed_name in ref_name_list:
                            if ref_name_list.index(parsed_name) == 1:
                                ad_name_index = data_chart_2.index(parsed_data)
                            else:
                                city_index = data_chart_2.index(parsed_data)
                    comparision_dict[key] = {
                        'text': TextUtil.compare_text(data_chart_2[city_index]['text'], data_chart_1[0]['text']),
                        'font': data_chart_2[city_index]['font'] == data_chart_1[0]['font'],
                        'size': abs(int(data_chart_2[city_index]['size']) - int(
                            data_chart_1[0]['size'])) < self.app_config.get_font_margin(),
                        'bbox': data_chart_2[city_index]['bbox'],
                        'text_details': {'parsed': data_chart_2[city_index]['text'],
                                         'reference': data_chart_1[0]['text']}}

                    comparision_dict['ad_name' if key == 'city' else 'ad_name_left'] = {
                        'text': TextUtil.compare_text(data_chart_2[ad_name_index]['text'], data_chart_1[1]['text']),
                        'font': data_chart_2[ad_name_index]['font'] == data_chart_1[1]['font'],
                        'size': abs(int(data_chart_2[ad_name_index]['size']) - int(
                            data_chart_1[1]['size'])) < self.app_config.get_font_margin(),
                        'bbox': data_chart_2[ad_name_index]['bbox'],
                        'text_details': {'parsed': data_chart_2[ad_name_index]['text'],
                                         'reference': data_chart_1[1]['text']}}


                elif key == 'filename':
                    ref_filename = data_chart_1[0]['text']

                    index_found = 0
                    for parsed_filename_data in data_chart_2:
                        parsed_filename = parsed_filename_data['text'].strip()
                        if parsed_filename == ref_filename:
                            index_found = data_chart_2.index(parsed_filename_data)
                            break

                    comparision_dict[key] = {
                        'text': TextUtil.compare_text(data_chart_2[index_found]['text'], data_chart_1[0]['text']),
                        'font': data_chart_2[index_found]['font'] == data_chart_1[0]['font'],
                        'size': abs(int(data_chart_2[index_found]['size']) - int(
                            data_chart_1[0]['size'])) < self.app_config.get_font_margin(),
                        'bbox': data_chart_2[index_found]['bbox'],
                        'text_details': {'parsed': data_chart_2[index_found]['text'],
                                         'reference': data_chart_1[0]['text']}}

                else:
                    comparision_dict[key] = {
                        'text': TextUtil.compare_text(data_chart_1[0]['text'], data_chart_2[0]['text']),
                        'font': data_chart_1[0]['font'] == data_chart_2[0]['font'],
                        'size': abs(int(data_chart_1[0]['size']) - int(
                            data_chart_2[0]['size'])) < self.app_config.get_font_margin(),
                        'bbox': data_chart_2[0]['bbox'],
                        'text_details': {'parsed': data_chart_2[0]['text'], 'reference': data_chart_1[0]['text']}}

            elif type(data_chart_1).__name__ == 'str':
                comparision_dict[key] = {'text': data_chart_1[key] == data_chart_2[key],
                                         'font': True,
                                         'size': True,
                                         'bbox': (0, 0, 0, 0)}

        return comparision_dict
