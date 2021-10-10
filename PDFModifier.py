import fitz

import os

class PDFMarker():
	def __init__(self, pdf_path, compared_data, out_path):
		self.pdf_path = pdf_path
		self.compared_data = compared_data
		#logger.log(logger.INFO, 'Processed PDF: {}, Comparison data: {}'.format(os.path.basename(self.pdf_path), self.compared_data))
		self.out_path = out_path

	def mark_pdf(self):
		try:
			doc = fitz.open(self.pdf_path)
			page = doc[0]
			print('compared data', self.compared_data)

			for key in self.compared_data:
				bbox = fitz.Rect(self.compared_data[key]['bbox'])
				if bbox == fitz.Rect(0,0,0,0):
					continue
				else:
					if self.compared_data[key]['text']:

						if self.compared_data[key]['text_details']['reference'] == '':
							continue
						rect_annot = page.add_rect_annot(bbox)
						if not self.compared_data[key]['font'] or not self.compared_data[key]['size']:
							rect_annot.set_colors(stroke=(1,1,0), fill=(1,1,0))
							rect_annot.set_opacity(0.8)
							rect_annot.update()
						else:
							rect_annot.set_colors(stroke=(0, 1, 0), fill=(0, 1, 0))
							rect_annot.set_opacity(0.8)
							rect_annot.update()
					else:
						rect_annot = page.add_rect_annot(bbox)
						rect_annot.set_colors(stroke= (1,0,0), fill = (1,0,0))
						rect_annot.set_opacity(0.6)
						rect_annot.update()

			doc.save(os.path.join(self.out_path,  os.path.basename(self.pdf_path)))
		except Exception as e:
			raise e

