
class CustomException(Exception):
	def __init__(self, message, exception_type):
		super().__init__(message)
		self.message = message
		self.exception_type = exception_type

	def get_message(self):
		return self.message

	def get_type(self):
		return self.exception_type 

class PDFPageCountException(CustomException):
	def __init__(self):
		super().__init__('A PDF must have a single page', self.__class__.__name__)

class FilenameLengthExcetion(CustomException):
	def __init__(self):
		super().__init__('Filename must contain 12 chars', self.__class__.__name__)

class FilenameExcetion(CustomException):
	def __init__(self):
		super().__init__('Last char of filename must be 0 or t or 1', self.__class__.__name__)

class ICAOException(CustomException):
	def __init__(self):
		super().__init__('ICAO must contain 4 chars', self.__class__.__name__)

class IATAException(CustomException):
	def __init__(self):
		super().__init__('IATA must contain 3 chars', self.__class__.__name__)

class NonSTDFrameException(CustomException):
	def __init__(self, msg):
		super().__init__('Non STD Frame: {}'.format(msg), self.__class__.__name__)

class UnknownChartSeriesException(CustomException):
	def __init__(self):
		super().__init__('Unknown chart series', self.__class__.__name__)

class UnknownICAOException(CustomException):
	def __init__(self):
		super().__init__('Unknown ICAO', self.__class__.__name__)

class BadInputException(CustomException):
	def __init__(self, msg):
		super().__init__('BadInputException: {}'.format(msg), self.__class__.__name__)