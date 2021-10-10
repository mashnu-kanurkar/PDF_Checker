from CustomExceptions import *
import fitz, json, airport_details

class Constants():

	def __init__(self):
		pass


	def get_chart_series(self, filename):
		chart_series_char = {'u': 4, 'l':10, 'g':10, 'v':20, 't':20, 'c': 30, 'd':30, 'a':40, 'i':50, 'm':51, 'p': 52, 'y': 55, 'h':53, 'z': 60}
		key = filename[6]
		if key in chart_series_char:
			return chart_series_char[key]
		else:
			raise UnknownChartSeriesException()

	def get_json_location(self):
		json_filename = '.\\App_config\\airport_details.json'
		try:
			file = open(json_filename, encoding='utf-8-sig')
			file.close()
			return json_filename
		except FileNotFoundError:
			default_airport_data = airport_details.get_default_airport_details()
			with open(json_filename, "w") as jsonFile:
				json.dump(default_airport_data, jsonFile)
			self.get_json_location()
		except Exception as e:
			raise e

	def get_copyright(self):
		return 'NAVBLUE'

	def chart_tab_bbox(self, filename):
		try:
			chart_series = self.get_chart_series(filename)
			is_backpage = int(filename[4:6])%2 == 0 
			#for back and front page , y will be same, x will have difference of 354
			#for every series y will have difference 73
			front_bbox = ()
			if int(chart_series) == 4:
				front_bbox = (379, 51, 395, 100)					
			elif int(chart_series) == 10:
				front_bbox = (379, 51, 395, 100)
				
			elif int(chart_series) == 20:
				front_bbox = (379, 124, 394, 170)
				
			elif int(chart_series) == 30:
				front_bbox = (379, 196, 394, 241)
				
			elif int(chart_series) == 40:
				front_bbox = (379, 267, 394, 314)
				
			elif int(chart_series) == 50:
				front_bbox = (379, 337, 394, 387)
				
			elif int(chart_series) == 51:
				front_bbox = (379, 409, 394, 456)

			elif int(chart_series) == 53:
				front_bbox = (379, 431, 395, 481)
				
			elif int(chart_series) == 60:
				front_bbox = (379, 431, 395, 481)
				
			if len(front_bbox) == 0:
				raise UnknownChartSeriesException()
			else:
				if is_backpage:
					return (front_bbox[0]-354, front_bbox[1], front_bbox[2]-354, front_bbox[3])
				else:
					return front_bbox
		except Exception as e:
			raise e

	def is_valid_pdf(self, doc):
		if len(doc) == 1:
			return True
		else:
			return False

	def get_bbox(self, pdf_path, filename):
		chart = (0, 0, 421, 595)
		general = (0.0, 0.0,  419, 595)
		a3_frame = (0.0, 0.0, 651.0, 595.0)
		doc = fitz.open(pdf_path)
		if self.is_valid_pdf(doc):
			page = doc[0]
			page.set_rotation(0)
			rect = fitz.Rect(page.bound())
			x0 = rect.x0
			y0 = rect.y0
			x1 = rect.x1
			y1 = rect.y1
			bound = (int(x0), int(y0), int(x1), int(y1))
			is_backpage = int(filename[4:6]) % 2 == 0
			if bound == fitz.Rect(chart):
				chart_tab_series_wise = self.chart_tab_bbox(filename)
				return {'wef':(75, 20, 153, 35), 'vao':(210, 19, 250, 35),
						'chart_num_top':(155, 19, 212, 35), 'country_icao_iata':(250, 19, 383, 35),
						'city':(208, 30, 385, 50), 'chart_num_tab':chart_tab_series_wise,
						'copyright':(29, 516, 38, 553), 'filename':(25, 450, 43, 515),
						'proc_criteria':(28, 191, 40, 250), 'amdt_num': (30, 390, 39, 420) if is_backpage else (30, 370, 39, 405)}
			elif bound == fitz.Rect(general):
				chart_tab_series_wise = self.chart_tab_bbox(filename)
				return {'wef':(75, 20, 167, 35), 'vao':(210, 20, 255, 35),
						'chart_num_top':(160, 20, 210, 35), 'country_icao_iata':(253, 21, 382, 34),
						'city':(209, 32, 382, 51), 'chart_num_tab':chart_tab_series_wise,
						'copyright':(25, 510, 41, 560), 'filename':(25, 450, 43, 510),
						'proc_criteria':(28, 191, 40, 250), 'amdt_num': (30, 390, 39, 420) if int(filename[4:6]) % 2 == 0 else (30, 370, 39, 405)}
			elif bound == fitz.Rect(a3_frame):
				return {'wef':(322, 22, 393, 32),
						'vao': (430, 23, 462, 32) ,
						'chart_num_top': (407, 23, 426, 32),
						'country_icao_iata': (465, 22, 597, 32),
						'city': (300, 31, 597, 47),
						'country_icao_iata_left': (54, 22, 320, 32),
						'city_left': (54, 31, 255, 47),
						'chart_num_tab': (0,0,0,0), 'copyright': (40, 516, 49, 553),
						'filename': (40, 470, 49, 514), 'proc_criteria': (0,0,0,0),
						'amdt_num': (0,0,0,0)} if is_backpage else {'wef': (215, 22, 286, 32),
						'vao':  (149, 23, 180, 32),
						'chart_num_top':  (126, 23, 144, 32),
						'country_icao_iata':  (290, 22, 597, 32),
						'city':  (300, 31, 596, 47),
						'chart_num_tab': (0,0,0,0), 'copyright': (40, 516, 49, 553),
						'filename': (40, 470, 49, 514), 'proc_criteria': (0,0,0,0),
						'amdt_num': (0,0,0,0)}
			else:
				raise NonSTDFrameException('Required {} found {}'.format(fitz.Rect(chart), page.bound()))
		else:
			raise PDFPageCountException()

	def path_to_save_output(self):
		out_path = ''
		return out_path

	font = {'wef': 'Helvetica-Bold', 'vao': 'Helvetica', 'chart_num_top': 'Helvetica-Bold', 'country_icao_iata': 'Helvetica',
			'city': 'Helvetica', 'ad_name': 'Helvetica', 'chart_num_tab': 'Helvetica-Bold', 'copyright': 'Helvetica',
			'filename': 'Helvetica', 'proc_criteria': 'Helvetica', 'amdt_num': 'Helvetica'}
	text_size = {'wef': 7, 'vao': 7, 'chart_num_top': 7, 'country_icao_iata': 7, 'city': 13, 'ad_name': 9,
				 'chart_num_tab': 11, 'copyright': 7, 'filename': 7, 'proc_criteria': 7, 'amdt_num': 7}



#can have advanced search like AD elev in all charts, highest obst, whitespace values  etc