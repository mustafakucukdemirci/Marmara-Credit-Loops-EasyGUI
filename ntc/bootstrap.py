import certifi
import urllib3
import tarfile
from PyQt5 import QtCore, QtGui, QtWidgets
import os

class bootStrapUpdate(QtCore.QThread):
    ssignal = QtCore.pyqtSignal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        url = "https://eu.bootstrap.dexstats.info/MCL-bootstrap.tar.gz"
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
        
        f = open(self.file_name, "wb")
        
        while True:
            buffer = r.read(block_sz)
            if not buffer:
                break
        
            file_size_dl += len(buffer)
            f.write(buffer)
            status = "{}".format(int(file_size_dl * 100. // file_size))
            self.ssignal.emit(status)
            #status = status + chr(8)*(len(status)+1)
            
        
        f.close()
        self.unpack()
    def unpack(self):
        
        with tarfile.open(self.file_name) as f:
            
            f.extractall(os.getenv("APPDATA")+"/Komodo/MCL")
        
           # Extract all the contents of zip file in current directory
        os.remove(self.file_name)
        

