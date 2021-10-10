import os
import sys
import PySide2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import *
#import your mainwindow object from generated *.py file
from main_pdf_processor import Ui_MainWindow

from Charts import *
from PDFModifier import PDFMarker
from Settings import AppConfig
import logger, time

# setup qt environment to avoid errors
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class Worker(QThread):
    """docstring for Worker"""
    def __init__(self, base_path, reference_data):
        super(Worker, self).__init__()
        self.base_path = base_path
        self.reference_data = reference_data
    
    # Create a  thread
    process_info = Signal(str, int)
    change_value = Signal(str, int , int)
    finished = Signal()

    def run(self):
        print('Thread started')
        
        for key in self.reference_data:
            try:
                print('Processing PDF - {}'.format(key))
                self.process_info.emit('Processing PDF - {}'.format(key), 0)

                chart1 = ReferenceChart(os.path.normpath(os.path.join(self.base_path, '{}.pdf'.format(key))), self.reference_data[key]['vao'], self.reference_data[key]['wef'], has_wef = self.reference_data[key]['has_wef'], country_icao_iata = self.reference_data[key]['country_icao_iata'], city = self.reference_data[key]['city'], ad_name = self.reference_data[key]['ad_name'] , copyright = self.reference_data[key]['copyright'], proc_criteria = self.reference_data[key]['proc_criteria'])
                chart2 = ChartToCheck(os.path.normpath(os.path.join(self.base_path, '{}.pdf'.format(key))))
                compared_charts = CompareCharts(chart1, chart2)
                compared_data = compared_charts.get_args_dict()
                info_error = 0
                other_error = 0
                for comparison_key in compared_data:
                    print('{}: {}'.format(comparison_key, compared_data[comparison_key]))
                    #print('{} - {}'.format(compared_key, 'Correct' if compared_data[compared_key] == 0 else 'Incorrect'))
                    if not compared_data[comparison_key]['text']:
                        info_error = info_error+1
                    if not compared_data[comparison_key]['font'] or not compared_data[comparison_key]['size']:
                        other_error = other_error +1

                self.change_value.emit(key, info_error, other_error)

                app_configuration = AppConfig()
                out = app_configuration.get_out_path()
                PDF_marker = PDFMarker(os.path.normpath(os.path.join(self.base_path, '{}.pdf'.format(key))), compared_data, out)
                PDF_marker.mark_pdf()

            except Exception as e:
                print('Exception: ', type(e))
                print('Exc args: ', e.args)
                logger.log(logger.EXCEPTION, e.args)
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                print("Exception type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)

                self.process_info.emit('Error occurred - {}'.format(e.args), 1)

        self.finished.emit()


class MyApp(Ui_MainWindow):
    
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.app_config = AppConfig(debug = False)
        app_config_path = '.\\App_config'

        if not os.path.exists(app_config_path):
            os.mkdir(app_config_path)
        # connections
        self.log_file_path = '.\\{}\\log'.format(app_config_path)

        if not os.path.exists(self.log_file_path):
            os.mkdir(self.log_file_path)

        self.delete_old_log()

        self.pushButton_check.clicked.connect(lambda:self.start_check())
        self.pushButton_remove.clicked.connect(lambda:self.removeSelected())
        self.pushButton_clear.clicked.connect(lambda:self.clear_all())
        self.checkBox_wef.clicked.connect(lambda: self.change_wef_state())
        self.pushButton_out_path.clicked.connect(lambda : self.set_out_path())

        if self.app_config.is_debug():
            self.set_debug_data()
        self.lineEdit_out_path.setText(self.app_config.get_out_path())

    def delete_old_log(self):
        interval = self.app_config.get_log_delete_interval()
        now = time.time()

        for f in os.listdir(self.log_file_path):
            file = os.path.join(self.log_file_path, f)
            if os.stat(file).st_mtime < (now - interval * 86400):
                if os.path.isfile(file):
                    os.remove(file)


    def set_debug_data(self):
        self.lineEdit_wef.setText('12 AUG 21 09:01')
        self.lineEdit_vao.setText('22 SEP 21')
        self.lineEdit_country_icao_iata.setText('Italy - LICZ / NSY')
        self.lineEdit_city.setText('CATANIA')
        self.lineEdit_ad_name.setText('Sigonella')

    def set_out_path(self):
        print(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        filepath = QtWidgets.QFileDialog.getExistingDirectory(None, os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        print(filepath)
        self.app_config.update_out_path(filepath)
        self.lineEdit_out_path.setText(filepath)

    
    def start_check(self):
        print("starting")

        self.textBrowser_status.setText('')
        self.textBrowser_results.setText('')
        if not self.validate_ref_data():
            print('Invalid ref data')
            return
        print('valid ref data')
        base_path = os.path.realpath(self.label_base_path.text().strip('/'))
        self.label_base_path.setText(base_path)

        reference_data = {}
        for index in range(self.listWidget_pdfs.count()):

            pdf_path = self.listWidget_pdfs.item(index).text()
            if not self.checkBox_wef.isChecked():
                self.listWidget_pdfs.item(index).setCheckState(QtCore.Qt.Unchecked)
            wef_check_state = True if self.listWidget_pdfs.item(index).checkState() == PySide2.QtCore.Qt.CheckState.Checked else False
            ref_wef = ''
            if wef_check_state:
                ref_wef = self.lineEdit_wef.text()
            amdt_num = ''
            if self.checkBox_amdt_num.isChecked():
                amdt_num = self.lineEdit_amdt_num.text()

            ref_ad_name = ''
            if self.checkBox_city.isChecked():
                ref_ad_name = self.lineEdit_city.text()

            reference_data[pdf_path] = ({'wef': ref_wef, 'vao': self.lineEdit_vao.text(), 'has_wef': wef_check_state,
                                         'country_icao_iata': self.lineEdit_country_icao_iata.text(),
                                         'city': self.lineEdit_city.text(), 'ad_name': ref_ad_name,
                                         'copyright': self.lineEdit_copyright.text(), 'proc_criteria': self.lineEdit_proc_criteria.text(),
                                         'amdt_num':amdt_num})

        self.thread = QThread()
        self.worker = Worker(base_path, reference_data)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.change_value.connect(self.log_details)
        self.worker.process_info.connect(self.log_status)
        self.thread.started.connect(self.log_status('Running analyser', 0))

        self.thread.start()
        self.pushButton_check.setEnabled(False)
        self.thread.finished.connect(lambda: self.pushButton_check.setEnabled(True))
        self.thread.finished.connect(lambda: self.log_status('Finished', 0))
            
            
    def log_status(self, msg_status, status_code):
        self.textBrowser_status.setAcceptRichText(True)
        if status_code == 0:
            self.textBrowser_status.append('<p style = "color: black">{}</p>'.format(msg_status))
        else:
            self.textBrowser_status.append('<p style = "color: red">{}</p>'.format(msg_status))


    def log_details(self, chart_name, info_error, other_error):
        self.textBrowser_results.setAcceptRichText(True)
        if info_error > 0 or other_error > 0:
            msg_details = '{}: {} {}'.format(chart_name, '{} info error. '.format(info_error) if info_error > 0 else '',
                                             '{} other error'.format(other_error) if other_error > 0 else '')
            if info_error > 0:
                red_text = '<p style = "color: red">{}</p>'.format(msg_details)
                self.textBrowser_results.append(red_text)
            elif other_error > 0:
                yellow_text = '<p style = "color: yellow">{}</p>'.format(msg_details)
                self.textBrowser_results.append(yellow_text)
        else:
            msg_details = '{}: no error found'.format(chart_name)
            black_text = '<p style = "color: black">{}</p>'.format(msg_details)
            self.textBrowser_results.append(black_text)

    def removeSelected(self):
        listItems = self.listWidget_pdfs.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.listWidget_pdfs.takeItem(self.listWidget_pdfs.row(item))

    def clear_all(self):
        self.listWidget_pdfs.clear()
        self.textBrowser_status.setText('')
        self.textBrowser_results.setText('')

    def change_wef_state(self):
        is_checked = self.checkBox_wef.isChecked();
        if is_checked:
            for index in range(self.listWidget_pdfs.count()):
                item = self.listWidget_pdfs.item(index)
                item.setCheckState(QtCore.Qt.Checked)
        else:
            for index in range(self.listWidget_pdfs.count()):
                item = self.listWidget_pdfs.item(index)
                item.setCheckState(QtCore.Qt.Unchecked)

    def validate_ref_data(self):
        if self.label_base_path.text() == '':
            self.show_error_msg('Base Path is empty')
            return False
        if self.checkBox_wef.isChecked():
            if self.lineEdit_wef.text() == '':
                self.show_error_msg('Please enter WEF date')
                return False

        if self.checkBox_wef.isChecked():
            if self.lineEdit_vao.text() == '':
                self.show_error_msg('Please enter VAO date')
                return False
        return True



    def show_error_msg(self, error_msg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(error_msg)
        msg.setWindowTitle("Error")
        msg.exec_()

if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    dialog = QtWidgets.QMainWindow()
    prog = MyApp(dialog)
    dialog.show()
    app.exec_()