import certifi
import urllib3
import zipfile
from PyQt5 import QtCore, QtGui, QtWidgets
import os,time
import subprocess

class Update(QtCore.QThread):
    ssignal = QtCore.pyqtSignal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        
        url = "http://marmara.io/guifiles/Win-MCL.zip"
        self.file_name = url.split('/')[-1]
        
        
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        
        r = http.request('GET', url, preload_content=False)
        
        file_size = int(r.headers["Content-Length"])
        
        print("Downloading: {} Bytes: {}".format(self.file_name, file_size))
        
        file_size_dl = 0
        block_sz = 8192
#
        f = open(self.file_name, "wb")
        
        while True:
            buffer = r.read(block_sz)
            if not buffer:
                break
        
            file_size_dl += len(buffer)
            f.write(buffer)
            status = "{}".format(int(file_size_dl * 100. // file_size))
            self.ssignal.emit(status)
        
        f.close()
        
        self.unpack()
    def unpack(self):
        
        self.ssignal.emit("Extracting Files...")
#        with zipfile.ZipFile(self.file_name, 'r') as zip_ref:
#            zip_ref.extractall(os.getenv("APPDATA")+"\\Komodo\\MCL\\Application Data")

        archive = zipfile.ZipFile(self.file_name)
        
        for file in archive.namelist():
            if file.startswith("fetch"):
                archive.extract(file, os.getenv("APPDATA")+"/Komodo/MCL/")
                print("file:",file,"  unzipped")
        archive.close()
        os.remove(self.file_name)
        self.ssignal.emit("DONE!")
        
        