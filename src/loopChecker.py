import subprocess
import json
import time
from PyQt5 import QtCore
import PyQt5

#Thread class that will write loops to a file
class writeLoops(QtCore.QThread):
    closedDict = {}
    openDict = {}
    SIGNAL = QtCore.pyqtSignal(object)
    
    def __init__(self,pubkey):
        QtCore.QThread.__init__(self)
        self.pubkey = pubkey
        
    def run(self):
        self.stop = False
        self.SIGNAL.emit([self.closedDict,self.openDict])
        while not self.stop:
            try:
                self.readFile()
                
                self.write()
                self.SIGNAL.emit([self.closedDict,self.openDict])
            except Exception as e :
                continue

    #check loops that already written.
    def readFile(self):
        try:
            with open("closedLoops.json","r") as a:
                x = json.loads(a.read())
                x = dict(x)
                for i,y in x.items():
                    self.closedDict[i] = y

        except:
            with open("closedLoops.json","w") as f:
                f.write("{}")
                x = {}
                f.close()


        try:
            with open("openLoops.json","r") as b:
                t = json.loads(b.read())
                t = dict(t)
                for i,y in t.items():
                    self.openDict[i] = y
        except:
            with open("openLoops.json","w") as c:
                c.write("{}")
                t = {}
                c.close()
        
	#check loop list. If loop not exist then 
	#receive info then write to file.
	def write(self):
        while True:
            try:
                x = subprocess.run("komodo-cli -ac_name=MCL marmarainfo 0 0 0 0 "+self.pubkey,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                x = str(x.stdout)[2:-5]
                x = x.replace("\\r","")
                x = x.replace("\\n","")
                _json = json.loads(x)
                break
            except:
                continue
		
        self.closedloopslist = list(_json["closed"])
        self.activeloopslist = list(_json["issuances"])
        
        
        
        for i in self.closedloopslist:
            if i not in self.closedDict.keys():
                output = subprocess.run("komodo-cli -ac_name=MCL marmaracreditloop "+i,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                output = str(output.stdout)[2:-5]
                output = output.replace("\\r","")
                output = output.replace("\\n","")
                self.closedDict[i] = json.loads(output)
                
                
        for x in self.activeloopslist:
            if x not in self.openDict.keys():
                output = subprocess.run("komodo-cli -ac_name=MCL marmaracreditloop "+x,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                output = str(output.stdout)[2:-5]
                output = output.replace("\\r","")
                output = output.replace("\\n","")
                self.openDict[i] = output

        
        with open("closedLoops.json","w") as f:
            
            f.write(json.dumps(self.closedDict,indent=4))
            
            
            
        with open("openLoops.json","w") as f:
            
            json.dump(self.openDict,f,indent=4)
            
    def stopper(self):
        self.stop= True
            


        