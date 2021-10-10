from CustomExceptions import *
from Constants import Constants
import json

class FilenameProcessor():
	def __init__(self, filename):
		self.filename = filename
		

	def varify_filename_length(self):
		if len(self.filename) == 12:
			pass
		else:
			raise FilenameLengthExcetion()

	def get_icao(self):
		try:
			self.varify_filename_length()
			return self.filename[:4].upper()
		except Exception as e:
			raise e

	def get_country(self):
		try:
			icao = self.get_icao()
			constants = Constants()
			f = open(constants.get_json_location(), encoding='utf-8-sig')
			data = json.loads(f.read())
			f.close()
			if icao.upper() in data:
				country = data[icao.upper()]['country']

				return country
			else:
				raise UnknownICAOException()
		except Exception as e:
			raise e

	def get_iata(self):
		try:
			icao = self.get_icao()
			constants = Constants()
			f = open(constants.get_json_location(), encoding='utf-8-sig')
			data = json.loads(f.read())
			f.close()
			if icao.upper() in data:
				iata = data[icao.upper()]['iata_code']
				return iata
			else:
				raise UnknownICAOException()
		except Exception as e:
			raise e

	def get_city(self):
		try:
			icao = self.get_icao()
			constants = Constants()
			f = open(constants.get_json_location(), encoding='utf-8-sig')
			data = json.loads(f.read())
			f.close()
			if icao.upper() in data:
				city = data[icao.upper()]['city']
				return city.upper()
			else:
				raise UnknownICAOException()
		except Exception as e:
			raise e

	def get_name(self):
		try:
			icao = self.get_icao()
			constants = Constants()
			f = open(constants.get_json_location(), encoding='utf-8-sig')
			data = json.loads(f.read())
			f.close()
			if icao.upper() in data:
				name = data[icao.upper()]['name']
				return name
			else:
				raise UnknownICAOException()
		except Exception as e:
			raise e

	def get_chart_number(self):
		try:
			self.varify_filename_length()
			number = int(self.filename[4:6])
			constants = Constants()
			series = constants.get_chart_series(self.filename)
			if self.filename[-1] == '0':
				return '{} - {}'.format(series, number)
			elif self.filename[-1] == 't':
				return '{} - {}T'.format(series, number)
			elif self.filename[-1] == '1':
				return '{} - 1 -{}'.format(series, number)
			else:
				raise FilenameExcetion()

		except Exception as e:
			raise e


	def is_back_page(self):
		try:
			return int(self.filename[4:6])%2 == 0

		except Exception as e:
			raise e
	def get_has_proc_criteria(self):
		try:
			constants = Constants()
			chart_series = constants.get_chart_series(self.filename)
			if int(chart_series) == 50:
				return True
			else:
				return False
		except Exception as e:
			raise e

	def get_has_amdt_num(self):
		try:
			constants = Constants()
			chart_series = constants.get_chart_series(self.filename)
			if int(chart_series) == 50:
				return True
			else:
				return False
		except Exception as e:
			raise e

class PDFPageProcessor():

	def get_bbox_dict(self):
		constants = Constants()
		return constants.get_bbox(self.page, self.filename)

class ManualDataProcessor():

	def __init__(self, filename, vao = '', wef = '', has_wef = True,
				 country_icao_iata = '', city = '', ad_name = '',
				 copyright = '©NAVBLUE', proc_criteria = 'PANS OPS', amdt_num = ''):
		self.filenameProcessor = FilenameProcessor(filename)
		self.icao = self.filenameProcessor.get_icao();
		if type(vao).__name__ == 'str':
			self.vao = vao
		else:
			raise BadInputException('VAO must be string object')
		if type(wef).__name__ == 'str':
			self.wef = wef
		else:
			raise BadInputException('WEF must be string object')

		if type(has_wef).__name__ == 'bool':
			self.has_wef = has_wef
		else:
			raise BadInputException('WEF must be string object')

		if type(country_icao_iata).__name__ == 'str':
			self.country_icao_iata = country_icao_iata
		else:
			raise BadInputException('country_icao_iata must be string object')

		if type(city).__name__ == 'str':
			self.city = city
		else:
			raise BadInputException('city must be string object')

		if type(ad_name).__name__ == 'str':
			self.ad_name = ad_name
		else:
			raise BadInputException('ad_name must be string object')

		if type(copyright).__name__ == 'str':
			self.copyright = copyright
		else:
			raise BadInputException('Copyright must be string object')

		if type(proc_criteria).__name__ == 'str':
			self.proc_criteria = proc_criteria
		else:
			raise BadInputException('PROC criteria must be string object')

		if type(amdt_num).__name__ == 'str':
			self.amdt_num = amdt_num
		else:
			raise BadInputException('AMDT number must be a string object')


	def get_vao(self):
		try:
			return self.vao
		except Exception as e:
			raise e

	def get_wef(self):
		try:
			if 'WEF' in self.wef:
				return self.wef
			else:
				return self.wef if self.wef == '' else 'WEF {}'.format(self.wef)
		except Exception as e:
			raise e
	def get_country_icao_iata(self):
		if self.country_icao_iata == '':
			return '{} - {} / {}'.format(self.filenameProcessor.get_country(), self.filenameProcessor.get_icao(), self.filenameProcessor.get_iata())
		else:
			return self.country_icao_iata

	def get_city(self):
		'''if self.city == '':
			return self.filenameProcessor.get_city()
		else:'''
		return self.city

	def get_ad_name(self):
		if self.ad_name == '':
			return self.filenameProcessor.get_name()
		else:
			return self.ad_name

	def get_copyright(self):
		try:
			if '-' in self.copyright:
				return  self.copyright
			else:
				return '{} -'.format(self.copyright)
		except Exception as e:
			raise e

	def get_has_wef(self):
		try:
			return self.has_wef
		except Exception as e:
			raise e

	def get_proc_criteria(self):
		try:
			has_procedure_criteria = self.filenameProcessor.get_has_proc_criteria()
			if has_procedure_criteria:
				return self.proc_criteria
			else:
				return ''
		except Exception as e:
			raise e

	def get_amdt_num(self):
		try:
			has_amdt_num = self.filenameProcessor.get_has_amdt_num()
			if has_amdt_num:

				if 'AMD ' in self.amdt_num:
					return self.amdt_num
				else:
					return self.amdt_num if self.amdt_num == '' else 'AMD {}'.format(self.amdt_num)
			else:
				return ''
		except Exception as e:
			raise e

	