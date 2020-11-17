import urllib.request
import xlrd
import csv
import os
import time
import multiprocessing

URL = 'http://coronavirus.saude.mg.gov.br/images/microdados/xlsx_painel.xlsx'
CSV_PATH = 'a_file.csv'

global downloading
downloading = False

global message
message = ""


class GetData:
    def __init__(self):
        self.process = multiprocessing.Process(target=process)

    def start_new(self):
        self.process = multiprocessing.Process(target=process)

    def start_process(self):
        if self.process.is_alive():
            pass
        else:
            try:
                self.process.start()
                return "started downloading..", "now..."
            except AssertionError as err:
                self.process.join()
                self.process.close()
                self.process = multiprocessing.Process(target=process)
                self.process.start()

                return "started downloading..", "now..."

    def get_process_status(self):
        return self.process.is_alive()


def process():
    sart = time.time()
    try:
        (path, ret) = urllib.request.urlretrieve(URL)
    except Exception:
        raise Exception(f"Erro ao baixar arquivo...{time.time() - sart}")

    try:
        with xlrd.open_workbook(path, encoding_override='utf-8') as wb:
            sh = wb.sheet_by_index(0)
            with open(CSV_PATH, 'w', newline="") as f:
                c = csv.writer(f)
                for r in range(sh.nrows):
                    c.writerow(sh.row_values(r))
    except Exception:
        raise Exception(f"Erro ao tratar arquivo csv...{time.time() - sart}")

    return CSV_PATH, f"modified: {time.ctime(os.path.getmtime(CSV_PATH))} - Tempo: {time.time() - sart}"


def get_data_from_web():
    sart = time.time()
    try:
        (path, ret) = urllib.request.urlretrieve(URL)
    except Exception:
        raise Exception(f"Erro ao baixar arquivo...{time.time() - sart}")

    try:
        with xlrd.open_workbook(path, encoding_override='utf-8') as wb:
            sh = wb.sheet_by_index(0)
            with open(CSV_PATH, 'w', newline="") as f:
                c = csv.writer(f)
                for r in range(sh.nrows):
                    c.writerow(sh.row_values(r))
    except Exception:
        raise Exception(f"Erro ao tratar arquivo csv...{time.time() - sart}")

    return CSV_PATH, f"modified: {time.ctime(os.path.getmtime(CSV_PATH))} - Tempo: {time.time() - sart}"


def get_path_date(path):

    try:
        ret = path, "modified: %s" % time.ctime(os.path.getmtime(CSV_PATH))
    except Exception as err:
        raise Exception(path, str(err))

    return ret
