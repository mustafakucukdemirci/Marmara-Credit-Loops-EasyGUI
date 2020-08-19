from PyQt5 import QtCore
import subprocess
import json
import time

class marmaraloops(QtCore.QThread):
    openLoops = []
    closedLoops = []
    signal = QtCore.pyqtSignal(object)
    requestsSignal = QtCore.pyqtSignal(object)
    requestcount = 0
    totalClosed = 0
    totalAmount = 0
    totalClosedSignal = QtCore.pyqtSignal(object)
    totalAmountSignal = QtCore.pyqtSignal(object)
    def __init__(self,pubkey,wallet):
        QtCore.QThread.__init__(self)
        self.__pubkey = pubkey
        self.__wallet = wallet

    def run(self):
        self.totalClosedSignal.emit(self.totalClosed)
        self.totalAmountSignal.emit(self.totalAmount)
        self.stop = False
        
        while not self.stop:
            try:
                x= subprocess.run("komodo-cli -ac_name=MCL marmarareceivelist "+self.__pubkey, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                x = str(x.stdout)[2:-5]
                x = x.replace("\\r","")
                x = x.replace("\\n","")
                
                self.loopRequests = json.loads(x)
                self.requestcount = len(self.loopRequests)
                self.signal.emit(self.requestcount)
                self.requestsSignal.emit(self.loopRequests)
                self.infoExecute()
                
                
            except:
                time.sleep(3)
                if(self.stop):
                    break
                pass
        
    def infoExecute(self):
        x = subprocess.run("komodo-cli -ac_name=MCL marmarainfo 0 0 0 0 "+self.__pubkey, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        x = str(x.stdout)[2:-5]
        x = x.replace("\\r","")
        x = x.replace("\\n","")
        self.json = json.loads(x)
        self.totalClosed = self.json["totalclosed"]
        self.totalAmount = self.json["totalamount"]
        try:
            self.ccadres
        except:
            self.ccadres = self.json["myCCAddress"]
         
        self.totalClosedSignal.emit(self.totalClosed)
        self.totalAmountSignal.emit(self.totalAmount)
        
    def stopThread(self):
        self.stop =True
        
        
