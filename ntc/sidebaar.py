from PyQt5.QtWidgets import *
from PyQt5 import QtCore

import PyQt5

import os
import subprocess
import time
import ast
from threading import Thread
import history
import json
from PyQt5.QtWidgets import *
from functools import partial
from PyQt5 import  QtGui, QtWidgets
import webbrowser
from playsound import playsound
import pyperclip
import sys
import bootstrap
import loopwindow
import loopChecker
import errorWindow


class commandExcuter(QtCore.QThread):
    _signal = QtCore.pyqtSignal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
    def exc(self,text,ConfirmBool,outputBool):
        x = subprocess.run(text, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        dialog = QtWidgets.QDialog()
        _dialog_window = errorWindow.Ui_dialog()
        _dialog_window.setupUi(dialog)
        _dialog_window.processCommand(x.stderr)
        
        if("error" in str(x.stdout)):
            self._signal.emit(x.stdout)
        
        x = str(x.stdout)[2:-5]
        x = x.replace("\\r","")
        x = x.replace("\\n","")
        
        if(ConfirmBool):
            ConfirmBool = subprocess.run("komodo-cli -ac_name=MCL sendrawtransaction "+x,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        if(outputBool):
            ConfirmBool = str(ConfirmBool.stdout)[2:-5]
            ConfirmBool = ConfirmBool.replace("\\r","")
            ConfirmBool = ConfirmBool.replace("\\n","")
            #self._signal.emit(ConfirmBool)
            return ConfirmBool
            
    
#check if 3x stake and boosted are activated once program started
class stake3x(QtCore.QThread):
    ssignal = QtCore.pyqtSignal(object)
    stake3x=False
    boosted=False
    myccaddress = ""
    def __init__(self,myccaddress):
        self.myccaddress = myccaddress
        QtCore.QThread.__init__(self)
    def emitter(self):
        self.ssignal.emit([self.stake3x,self.boosted])
    def run(self):
        try:
            x = subprocess.run("komodo-cli -ac_name=MCL marmaraposstat 0 0 | grep "+' \"'+self.myccaddress+'\"'+" -A10", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            _json = "{"+ str(x.stdout)[2:-5]+"\"}"
            _json= _json.replace("\\n","")
            _json = _json.replace(" ","")
            
            
            i = 0
            
            while i < len(_json)-1:
                if(_json[i]==":" and _json[i+1] != '"'):
                    _json = _json[0:i+1] + '"' + _json[i+1:]
                    i+= 1
                if(_json[i]=="," and _json[i-1] != '"' and _json[i-1] != "}"):
                    _json = _json[0:i] + '"' + _json[i:]
                    i+=1
                if(_json[i]=="}" and _json[i-1]!='"' ):
                    _json = _json[0:i] +'"' + _json[i:]
                    i+=1
                
                
                i+=1
            i=0
            while i < len(_json)-1:
                if(_json[i]=="{" and _json[i-1] == "," and _json[i-2] == "}"):
                    _json = _json[:i-1] +"|" + _json[i:]
                i+=1
            
            
            _json = _json.split("|")
            for i in _json:
                _json = json.loads(i)
                if(_json["StakeTxAddress"] == self.myccaddress and ("3x" in _json["StakeTxType"]) ):
                    self.stake3x=True
                if(_json["StakeTxAddress"] == self.myccaddress and ("boosted" in _json["StakeTxType"]) ):
                    self.boosted=True
            self.emitter()
        except:
            self.emitter()
        
#labels over loading bar at bottem right.
class DownloadThread(QtCore.QThread):

    printvalues = QtCore.pyqtSignal(object)
    text = "connecting to chain"
    value = 0

    def __init__(self):
        QtCore.QThread.__init__(self)

    def emitter(self):
        data = [self.text,self.value]
        self.printvalues.emit(data)
    def run(self):
        self.progressbar()
    
    def progressbar(self):
        self.stop_thread = False
        while(not self.stop_thread):
            try:
                x = subprocess.run("komodo-cli -ac_name=MCL getblockcount", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                
                _json = str(x.stdout)[2:-5]
                
                y = subprocess.run("komodo-cli -ac_name=MCL getinfo | findstr longestchain", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                
                __json = str(y.stdout)[2:-5]
                __json = __json.split(":")
                __json = __json[1]
                __json = __json.replace(" ","")
                __json = __json.replace(",","")
                self.value = float(float(_json)/float(__json)) *100
                self.text = str("Loading blocks...  "+str(int(self.value))+"%  "+_json+"/"+__json)
                
                
                
                
                self.emitter()
                    
            except Exception as e:
                self.text = "connecting to chain"
                self.value = 100
                self.emitter()
                
                pass
            time.sleep(0.25)
    def stopThread(self):
        self.stop = True

#check mining and staking status on a cycle
class MiningStatus(QtCore.QThread):

    miningssignal = QtCore.pyqtSignal(object)
    miningtext = "connecting..."
    stakingtext = "connecting..."

    def __init__(self):
        QtCore.QThread.__init__(self)

    def emitter(self):
        
        self.miningssignal.emit([self.miningtext,self.stakingtext])

    def run(self):
        self.process()
        
    def process(self):
        self.stop = False
        while not self.stop:
            try:
                self.emitter()
                x = subprocess.run("komodo-cli -ac_name=MCL getgenerate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                
                _json = str(x.stdout)[2:-5]
                _json = _json.replace("true",'"true"')
                _json = _json.replace("false",'"false"')
                _json = _json.replace("\\r","")
                _json = _json.replace("\\n","")
                _json = json.loads(_json)
                
                
                self.stakingtext = _json["staking"]
                self.miningtext = _json["generate"]
                
            except Exception as e:
                self.stakingtext = "connecting..."
                self.miningtext = "connecting..."
                self.emitter()
                time.sleep(1)
                continue
    def stopThread(self):
        self.stop = True
        
#called when we query a loop
class LoopControlThread(QtCore.QThread):

    loopssignal = QtCore.pyqtSignal(object)
    x = ""
    txid = ""
    def __init__(self):
        QtCore.QThread.__init__(self)

    def emitter(self):
        
        self.loopssignal.emit(self.x)

    def run(self):
        self.process()
    def setTxid(self,Txid):
        self.txid = Txid
    def process(self):
        try:
            self.x = subprocess.run("komodo-cli -ac_name=MCL marmaracreditloop "+self.txid,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            self.emitter()
        except:
            pass

#history process.
class updateHistory(QtCore.QThread):

    historysignal = QtCore.pyqtSignal(object)
    __hist = []
    __walletaddress = ""
    def __init__(self):
        QtCore.QThread.__init__(self)

    def emitter(self):
        self.historysignal.emit(self.__hist)

    def definewallet(self,address):
        self.__walletaddress = address
    def run(self):
        self.emitter()
        self.process()
        
    def process(self):
        self.stop = False
        
        while (not self.stop):
            try:
                if(temp != len(self.__hist)):
                    self.emitter()
                    time.sleep(10)
                    
                temp = len(self.__hist)
                
            except:
                temp = len(self.__hist)
                pass
            try:
                self.__hist = history.run(self.__walletaddress)
                time.sleep(1)
                
            except Exception as e:
                time.sleep(3)
                continue
            
    def stopThread(self):
        self.stop = True
        
#qprogressbar inherited to manage text over bar.
class MyProgressBar(QtWidgets.QProgressBar):
    def __init__(self):
        super().__init__()
        self.setRange(0, 100)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self._text = None

    def setText(self, text):
        self._text = text

    def text(self):
        return self._text



class Window(QMainWindow):
    #inialitize main window    
    def __init__(self):
        super().__init__()
        self.stop = False
                
        self.setStyleSheet("background-color:rgb(51,51,51)")
        self.setStyle(QStyleFactory.create('Fusion'))
        # set the title of main window
        self.setWindowTitle('EasyGUI for MCL')

        # set the size of window
        self.setFixedSize(1200,700)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 1200, 700))
    #open mining
    def setLang(self,lang):
        self.lang = lang
    def openMining(self):
        if(self.miningstatustext.text() == "ON"):
            self.closeMiningStaking()
        else:
            subprocess.run("komodo-cli -ac_name=MCL setgenerate true 1",  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    #open staking
    def openStaking(self):
        if(self.stakingstatustext.text() == "ON"):
            self.closeMiningStaking()
        else:
            subprocess.run("komodo-cli -ac_name=MCL setgenerate true 0",  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    #close staking and mining
    def closeMiningStaking(self):
        subprocess.run("komodo-cli -ac_name=MCL setgenerate false", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    #TODO:make openStaking/Mining core numbers optional
    
    #Main wallet screen.
    #TODO: change this pubkey with CC address to prevent confusion.
    def mainInfos(self):
        self.clearCoinScreen()
         
        
    def sendCoinScreen(self):
        
        self.clearCoinScreen()
        adreslabel = QtWidgets.QLabel("Adres:")
        adreslabel.setStyleSheet("color:white;font-size:16pt")
        
        self.walletGroupBoxLayout.addWidget(adreslabel,0,0)
        
        self.adrestext = QtWidgets.QLineEdit()
        self.adrestext.setStyleSheet("color:white")
        self.walletGroupBoxLayout.addWidget(self.adrestext,0,1,1,5)
        
        amountlabel = QtWidgets.QLabel("Miktar")
        amountlabel.setStyleSheet("color:white;font-size:16pt")
        self.walletGroupBoxLayout.addWidget(amountlabel,1,0)
        
        self.amountlabeltext = QtWidgets.QLineEdit()
        self.amountlabeltext.setStyleSheet("color:white")
        self.walletGroupBoxLayout.addWidget(self.amountlabeltext,1,1,1,5)
        
        backbutton = QtWidgets.QPushButton()
        backbutton.setText(self.lang["back"])
        backbutton.clicked.connect(self.mainInfos)
        self.walletGroupBoxLayout.addWidget(backbutton,5,3)
        
        sendbutton = QtWidgets.QPushButton()
        sendbutton.setText(self.lang["send"])
        sendbutton.clicked.connect(self.sendCoinCommand)
        self.walletGroupBoxLayout.addWidget(sendbutton,5,2)
    
    
#    def setupErrorMessage(self,text):
#        print(text)
#        dialog = QtWidgets.QDialog()
#        _dialog_window = errorWindow.Ui_dialog()
#        _dialog_window.setupUi(dialog)
#        _dialog_window.processCommand(text)
        
    def sendCoinCommand(self):
        sendCommand = commandExcuter()
        sendCommand.exc("komodo-cli -ac_name=MCL sendtoaddress "+str(self.adrestext.text())+" "+str(self.amountlabeltext.text()),True,False)
        
        
#    def __sendCoinCommand(self):
#        x = subprocess.run("komodo-cli -ac_name=MCL sendtoaddress "+str(self.adrestext.text())+" "+str(self.amountlabeltext.text()), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
#        
#
#        x = str(x.stdout)[2:-5]
#        x = x.replace("\\r","")
#        x = x.replace("\\n","")
#        subprocess.run("komodo-cli -ac_name=MCL sendrawtransaction "+x,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
#    
#        
    def lockCoinScreen(self):
        
        self.clearCoinScreen()
        
        amountlabel = QtWidgets.QLabel("Miktar")
        amountlabel.setStyleSheet("color:white;")
        self.walletGroupBoxLayout.addWidget(amountlabel,0,0)
        
        self.amounttext = QtWidgets.QLineEdit()
        self.amounttext.setStyleSheet("color:white;")
        self.walletGroupBoxLayout.addWidget(self.amounttext,0,1,1,5)
        
        backbutton = QtWidgets.QPushButton()
        backbutton.setText(self.lang["back"])
        backbutton.clicked.connect(self.mainInfos)
        self.walletGroupBoxLayout.addWidget(backbutton,5,4)
        
        lockbutton = QtWidgets.QPushButton()
        lockbutton.setText(self.lang["lock"])
        lockbutton.clicked.connect(self.lockCoin)
        self.walletGroupBoxLayout.addWidget(lockbutton,5,2)
        
        unlockbutton = QtWidgets.QPushButton()
        unlockbutton.setText(self.lang["unlock"])
        unlockbutton.clicked.connect(self.unlockCoin)
        self.walletGroupBoxLayout.addWidget(unlockbutton,5,3)
    
    def lockCoin(self):
        self.clearCoinScreen()
        #BURADA KALDIM

        sendCommand = commandExcuter()
        sendCommand._signal.connect(self.printCoinError)
        sendCommand.exc("komodo-cli -ac_name=MCL marmaralock "+str(self.amounttext.text()),True,True)

            
        
        
    def unlockCoin(self):
        self.clearCoinScreen()
        
        sendCommand = commandExcuter()  
        sendCommand._signal.connect(self.printCoinError)
        sendCommand.exc("komodo-cli -ac_name=MCL marmaraunlock "+str(self.amounttext.text()),True,True)
        

    def printCoinError(self,txt):
        dialog = QtWidgets.QDialog()
        _dialog_window = errorWindow.Ui_dialog()
        _dialog_window.setupUi(dialog)
        _dialog_window.processCommand(txt[1:-2])
        
    def miningCoinScreen(self):
        
        self.clearCoinScreen()
        
        backbutton = QtWidgets.QPushButton(self.gridLayoutWidget)
        backbutton.setText(self.lang["back"])
        backbutton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding-top:20px;padding-bottom:20px")
        backbutton.setGeometry(QtCore.QRect(2, 19, 326, 73))
        backbutton.clicked.connect(self.mainInfos)
        backbutton.setGeometry(QtCore.QRect(2, 19, 352, 78))
        self.walletGroupBoxLayout.addWidget(backbutton,5,1,2,2)
        
        openMiningButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        openMiningButton.setText(self.lang["open_mining"])
        openMiningButton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding-top:20px;padding-bottom:20px")
        openMiningButton.setGeometry(QtCore.QRect(2, 19, 326, 73))
        openMiningButton.clicked.connect(lambda x:self.__strExcuter("""subprocess.run("komodo-cli -ac_name=MCL setgenerate true 1",  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)"""))
        self.walletGroupBoxLayout.addWidget(openMiningButton,0,0,2,2)
        
        closeMiningButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        closeMiningButton.setText(self.lang["close_mining"])
        closeMiningButton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding-top:20px;padding-bottom:20px")
        closeMiningButton.setGeometry(QtCore.QRect(2, 19, 326, 73))
        closeMiningButton.clicked.connect(lambda x:self.__strExcuter("""subprocess.run("komodo-cli -ac_name=MCL setgenerate false",  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)"""))

        self.walletGroupBoxLayout.addWidget(closeMiningButton,0,2,2,2)
        
        openStakingButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        openStakingButton.setText(self.lang["open_staking"])
        openStakingButton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding-top:20px;padding-bottom:20px")
        openStakingButton.setGeometry(QtCore.QRect(2, 19, 326, 73))
        openStakingButton.clicked.connect(lambda x:self.__strExcuter("""subprocess.run("komodo-cli -ac_name=MCL setgenerate true 0",  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)"""))
        self.walletGroupBoxLayout.addWidget(openStakingButton,2,0,2,2)
        
        closeStakingButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        closeStakingButton.setText(self.lang["close_staking"])
        closeStakingButton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding-top:20px;padding-bottom:20px")
        closeStakingButton.setGeometry(QtCore.QRect(2, 19, 326, 73))
        closeStakingButton.clicked.connect(lambda x:self.__strExcuter("""subprocess.run("komodo-cli -ac_name=MCL setgenerate false",  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)"""))
        self.walletGroupBoxLayout.addWidget(closeStakingButton,2,2,2,2)
        
    def __strExcuter(self,string):
        Thread(target=lambda: exec(string),).start()
        
    def clearCoinScreen(self):
        layout = self.walletGroupBoxLayout
        while layout.count():
            child = layout.takeAt(0)
            child.widget().deleteLater()
            del child
    #######################################################################################
    def setpubkey(self,pubkey):
        self.__pubkey = pubkey
    def setWalletAddress(self,address):
        self.__walletaddress = address

    def progressbar_update(self, data):
        self.progressbar.setText(data[0])
        self.progressbar.setProperty("value", int(data[1]))
        self.progressbar.update() 
        if("connecting" not in data[0]):
            self.groupBox.setEnabled(True)
            
            
    def update3xboosted(self,liste):
        if(liste[0] == True):
            self.staking3Xtext.setText(self.lang["on"])
            self.staking3Xtext.setStyleSheet("color:green;font-size:14pt;border:0px")
            self.staking3Xtext.update()
        else:
            self.staking3Xtext.setText(self.lang["off"])
            self.staking3Xtext.setStyleSheet("color:red;font-size:14pt;border:0px;")
            self.staking3Xtext.update()
        if(liste[1] == True):
            self.boostedtext.setText(self.lang["on"])
            self.boostedtext.setStyleSheet("color:green;font-size:14pt;border:0px")
            self.boostedtext.update()
        else:
            self.boostedtext.setText(self.lang["off"])
            self.boostedtext.setStyleSheet("color:red;font-size:14pt;border:0px;")
            self.boostedtext.update()            
            
        
    def updateMiningStaking(self,liste):
        
        miningtext = liste[0]
        if(miningtext=="false"):
            self.miningstatustext.setText(self.lang["off"])
            self.miningstatustext.setStyleSheet("color:red;font-size:14pt;border:0px;")
        elif(miningtext=="true"):
            self.miningstatustext.setText(self.lang["on"])
            self.miningstatustext.setStyleSheet("color:green;font-size:14pt;border:0px;")
        else:
            self.miningstatustext.setText(self.lang["connecting"])
            self.miningstatustext.setStyleSheet("color:orange;font-size:14pt;border:0px;")
        stakingtext =liste[1]
        if(stakingtext=="false"):
            self.stakingstatustext.setText(self.lang["off"])
            self.stakingstatustext.setStyleSheet("color:red;font-size:14pt;border:0px")
        elif(stakingtext=="true"):
            self.stakingstatustext.setText(self.lang["on"])
            self.stakingstatustext.setStyleSheet("color:green;font-size:14pt;border:0px")
        else:
            self.stakingstatustext.setText(self.lang["connecting"])
            self.stakingstatustext.setStyleSheet("color:orange;font-size:14pt;border:0px")
            
    def updateLoopRequests(self,count):
        
        self.looprequestscount.setText(str(count))
        self.looprequestscount.update()
        

        
    def connectToChain(self):
        count = 20
        while count>0:
            count -=1
            self.wallet_adress = subprocess.run("komodo-cli -ac_name=MCL getinfo", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            self.wallet_adress = str(self.wallet_adress.stdout)[2:-5]
            self.wallet_adress = self.wallet_adress.replace("\\r\\n","")
            if(self.wallet_adress == "" or "error" in self.wallet_adress ):
                subprocess.run("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 -pubkey="+self.__pubkey,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                continue
            else:
                break
            time.sleep(3)

        
        Thread(target=self.__staker,args=(self.wallet_adress,)).start()
    def __staker(self,adres):
        try:
            stake_ = stake3x(adres)
            stake_.ssignal.connect(self.update3xboosted)
            stake_.start()
            stake_.wait()
        except Exception as e:
            print(e)
            pass
        
    
    def initUI(self):

        Thread(target=self.connectToChain).start()
        
        self.loops = loopwindow.marmaraloops(self.__pubkey,self.__walletaddress )
        self.loops.signal.connect(self.updateLoopRequests)
        self.loops.requestsSignal.connect(self.updateRequests)
        self.loops.totalAmountSignal.connect(self.__settotalAmount)
        self.loops.totalClosedSignal.connect(self.__settotalClosed)
        self.loops.start()
        
        
        self.loopTables = loopChecker.writeLoops(self.__pubkey)
        self.loopTables.SIGNAL.connect(self.__LoopsUpdate)
        self.loopTables.start()
        
        

        balance = Thread(target=self.get_balance)
        balance.setDaemon(True)
        balance.start()
        
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 50, 151, 710))
        self.groupBox.setStyleSheet("color:gray;background-color:rgb(51,51,51)")
        
        
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(5, 3, 1180, 61))
        self.groupBox_2.setStyleSheet("border:1px solid rgb(80,80,80);color:gray;background-color:rgb(51,51,51);")
        
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10,5, 505, 25))
        self.groupBox_3.setStyleSheet("color:gray;background-color:rgb(51,51,51);")
        
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(520, 5, 210, 25))
        self.groupBox_4.setStyleSheet("color:gray;background-color:rgb(51,51,51);")
        
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setGeometry(QtCore.QRect(735, 5, 210, 25))
        self.groupBox_5.setStyleSheet("color:gray;background-color:rgb(51,51,51);")
        
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_9.setGeometry(QtCore.QRect(950, 5, 210, 52))
        self.groupBox_9.setStyleSheet("color:gray;background-color:rgb(51,51,51);")
        
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setGeometry(QtCore.QRect(10,32, 505, 25))
        self.groupBox_6.setStyleSheet("color:gray;background-color:rgb(51,51,51);")
        
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_7.setGeometry(QtCore.QRect(520, 32, 210, 25))
        self.groupBox_7.setStyleSheet("color:gray;background-color:rgb(51,51,51);")
        
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_8.setGeometry(QtCore.QRect(735, 32, 210, 25))
        self.groupBox_8.setStyleSheet("color:gray;background-color:rgb(51,51,51);")

        
        self.normalAddressLabel = QtWidgets.QLabel(self.groupBox_3)
        self.normalAddressLabel.setText(self.lang["address"])
        self.normalAddressLabel.setStyleSheet("color:white;font-size:13pt;border:0px")
        self.normalAddressLabel.setGeometry(QtCore.QRect(13, 1, 80, 23))
        self.normalAddressLabel.mouseReleaseEvent = self.copyAddressToClipboard
        self.normalAddressLabel.setToolTip(self.lang["click_to_copy_address"])
    
        self.normalAddressLabel_2 = QtWidgets.QLabel(self.groupBox_3)
        self.normalAddressLabel_2.setText(self.__walletaddress)
        self.normalAddressLabel_2.setStyleSheet("color:white;font-size:13pt;border:0px")
        self.normalAddressLabel_2.setGeometry(QtCore.QRect(93, 1, 405, 23))
        self.normalAddressLabel_2.mouseReleaseEvent = self.copyAddressToClipboard
        self.normalAddressLabel_2.setToolTip(self.lang["click_to_copy_address"])
        
        self.pubkeyLabel = QtWidgets.QLabel(self.groupBox_6)
        self.pubkeyLabel.setText(self.lang["pubkey"])
        self.pubkeyLabel.setStyleSheet("color:white;font-size:13pt;border:0px")
        self.pubkeyLabel.setGeometry(QtCore.QRect(13, 1, 80, 23))
        self.pubkeyLabel.setToolTip(self.lang["click_to_copy_pubkey"])
        self.pubkeyLabel.mouseReleaseEvent = self.copyPubkeyToClipboard
        
        self.pubkeyLabelText = QtWidgets.QLabel(self.groupBox_6)
        self.pubkeyLabelText.setText(self.__pubkey[:40]+"...")
        self.pubkeyLabelText.setStyleSheet("color:white;font-size:13pt;border:0px")
        self.pubkeyLabelText.setGeometry(QtCore.QRect(110, 1, 405, 23))
        self.pubkeyLabelText.setToolTip(self.lang["click_to_copy_pubkey"])
        self.pubkeyLabelText.mouseReleaseEvent = self.copyPubkeyToClipboard
        
        
        
        self.miningtext = QtWidgets.QLabel(self.groupBox_4)
        self.miningtext.setText(self.lang["mining"])
        self.miningtext.setStyleSheet("color:white;font-size:14pt;border:0px;")
        self.miningtext.setGeometry(QtCore.QRect(13, 1, 65, 23))
        
        self.miningstatustext = QtWidgets.QLabel(self.groupBox_4)
        self.miningstatustext.setGeometry(QtCore.QRect(75, 1, 120, 23))
        self.miningstatustext.setStyleSheet("font-size:14pt;border:0px;")
        
        self.staking3X = QtWidgets.QLabel(self.groupBox_7)
        self.staking3X.setText(self.lang["3xstaking"])
        self.staking3X.setStyleSheet("color:white;font-size:14pt;border:0px;")
        self.staking3X.setGeometry(QtCore.QRect(13, 1, 85, 23))
        
        self.staking3Xtext = QtWidgets.QLabel(self.groupBox_7)
        self.staking3Xtext.setGeometry(QtCore.QRect(100, 1, 100, 23))
        self.staking3Xtext.setText(self.lang["connecting"])
        self.staking3Xtext.setStyleSheet("font-size:14pt;border:0px;color:orange;")
        
        
        self.stakingtext = QtWidgets.QLabel(self.groupBox_5)
        self.stakingtext.setText(self.lang["staking"])
        self.stakingtext.setStyleSheet("color:white;font-size:14pt;border:0px")
        self.stakingtext.setGeometry(QtCore.QRect(13, 1, 70, 23))
        
        self.stakingstatustext = QtWidgets.QLabel(self.groupBox_5)
        self.stakingstatustext.setGeometry(QtCore.QRect(80, 1, 120, 23))
        self.stakingstatustext.setText(self.lang["connecting"])
        self.stakingstatustext.setStyleSheet("font-size:14pt;border:0px;color:orange;")
        
        
        self.boosted = QtWidgets.QLabel(self.groupBox_8)
        self.boosted.setText(self.lang["boosted"])
        self.boosted.setStyleSheet("color:white;font-size:14pt;border:0px;")
        self.boosted.setGeometry(QtCore.QRect(13, 1, 73, 23))
        
        self.boostedtext = QtWidgets.QLabel(self.groupBox_8)
        self.boostedtext.setGeometry(QtCore.QRect(90, 1, 115, 23))
        self.boostedtext.setText(self.lang["connecting"])
        self.boostedtext.setStyleSheet("font-size:14pt;border:0px;color:orange")
        
        
        self.looprequeststext = QtWidgets.QLabel(self.groupBox_9)
        self.looprequeststext.setText(self.lang["loop_requests"]+":")
        self.looprequeststext.setGeometry(QtCore.QRect(10, 9, 135, 30))
        self.looprequeststext.setStyleSheet("color:white;font-size:14pt;border:0px")
        
        self.looprequestscount = QtWidgets.QLabel(self.groupBox_9)
        self.looprequestscount.setText("...")
        self.looprequestscount.setGeometry(QtCore.QRect(150, 9, 30, 30))
        self.looprequestscount.setStyleSheet("color:white;font-size:14pt;border:0px")
        
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(151, 65, 1000, 689))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.GridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.GridLayout.setContentsMargins(0, 0, 0, 0)
        
        self.progressbarlabel = QtWidgets.QLabel()
        self.progressbarlabel.setParent(self.centralwidget)
        self.progressbarlabel.setText(self.lang["blocks"])
        self.progressbarlabel.setGeometry(QtCore.QRect(300, 689, 200,11))
        self.progressbarlabel.setStyleSheet("color:white")
        
        
        
        self.progressbar = MyProgressBar()
        self.progressbar.setParent(self.centralwidget)
        self.progressbar.setProperty("value", 1)
        self.progressbar.setGeometry(QtCore.QRect(400, 689, 800,11))
        
        
        
        self.miningstatus = MiningStatus()
        self.miningstatus.miningssignal.connect(self.updateMiningStaking)
        self.miningstatus.start()
        
        
        self.Threader = DownloadThread()
        self.Threader.printvalues.connect(self.progressbar_update)
        self.Threader.start()
        

        #self.GridLayout.addWidget(self.progressbar)
        
        self.historyAgent = updateHistory()
        self.historyAgent.definewallet(self.__walletaddress)
        self.historyAgent.historysignal.connect(self.newHistory)
        self.historyAgent.start()
        
        # add all widgets
        self.btn_1 = QtWidgets.QPushButton(self.groupBox)
        self.btn_1.setStyleSheet("color:gray;border:0;font-size:18px")
        self.btn_1.setGeometry(QtCore.QRect(0, 180, 150,50))
        self.btn_1.setText(self.lang["wallet"])

        
        self.btn_2 = QtWidgets.QPushButton(self.groupBox)
        self.btn_2.setStyleSheet("color:gray;border:0;font-size:18px")
        self.btn_2.setGeometry(QtCore.QRect(0, 230, 150,50))
        self.btn_2.setText(self.lang["credit_loops"])
        
        self.btn_3 = QtWidgets.QPushButton(self.groupBox)
        self.btn_3.setStyleSheet("color:gray;border:0;font-size:18px")
        self.btn_3.setGeometry(QtCore.QRect(0, 280, 150,50))
        self.btn_3.setText(self.lang["setting"])
        
        self.btn_4 = QtWidgets.QPushButton(self.groupBox)
        self.btn_4.setStyleSheet("color:gray;border:0;font-size:18px")
        self.btn_4.setGeometry(QtCore.QRect(0, 330, 150,50))
        self.btn_4.setText(self.lang["exit"])
        
        
        
        
        
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.closeEvent)
        
        
        self.bootstrapQGtitle = "Download BootStrap"#bootstraptitle in settings part
        self.bootstrapprogressvalue = 0
        
        self.setCentralWidget(self.centralwidget)
        
        self.button1()

    def clear(self):
        layout = self.GridLayout
        while layout.count():
            child = layout.takeAt(0)
            child.widget().deleteLater()
            del child


    def clearContentScreen(self):
        layout = self.contentLayoutManagement
        while layout.count():
            child = layout.takeAt(0)
            child.widget().deleteLater()
            del child


    def button1(self):
        
        self.clear()
        self.currentMenu("wallet")
        
        self.balance1 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.balance1.setTitle(self.lang["normal_Amount"])
        self.balance1.setStyleSheet("QGroupBox::title{color:white;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
#        self.balance1.setStyleSheet("QGroupBox::title{color:white;border: 1px solid gray;subcontrol-origin: margin;subcontrol-position: top center;padding-left:70px;padding-right:65px;margin-top:2px;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.balance1.setAlignment(QtCore.Qt.AlignCenter)

#        self.balance1.setStyleSheet("font: 12pt;border:1px solid gray;subcontrol-origin: margin;subcontrol-position: top center;padding-left:82px;padding-right:80px;padding-top:3px;padding-bottom:3px;")

        
        self.balance2 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.balance2.setTitle(self.lang["active_Amount"])
#        self.balance2.setStyleSheet("QGroupBox::title{color:white;border: 1px solid gray;subcontrol-origin: margin;subcontrol-position: top center;padding-left:79px;padding-right:73px;margin-top:2px;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.balance2.setStyleSheet("QGroupBox::title{color:white;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.balance2.setAlignment(QtCore.Qt.AlignCenter)

        
        self.balance3 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.balance3.setTitle(self.lang["wallet_Amount"])
#        self.balance3.setStyleSheet("QGroupBox::title{color:white;border: 1px solid gray;subcontrol-origin: margin;subcontrol-position: top center;padding-left:65px;padding-right:61px;margin-top:2px;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.balance3.setStyleSheet("QGroupBox::title{color:white;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.balance3.setAlignment(QtCore.Qt.AlignCenter)

        
        
        self.balance4 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.balance4.setTitle(self.lang["total_locked_amount"])
#        self.balance4.setStyleSheet("QGroupBox::title{color:white;border: 1px solid gray;subcontrol-origin: margin;subcontrol-position: top center;padding-left:54px;padding-right:49px;margin-top:2px;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.balance4.setStyleSheet("QGroupBox::title{color:white;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.balance4.setAlignment(QtCore.Qt.AlignCenter)

        
        self.history_tab()

        self.label = QtWidgets.QLabel()
        self.label.setGeometry(QtCore.QRect(0, 50, 50,50))
        self.label.setText("\n\n\n")
        
        
        
        normalamount = str(self.normalamount)
        self.amount_label = QtWidgets.QLabel(self.balance1)
        self.amount_label.setGeometry(8,27,210,40)
        self.amount_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amount_label.setText(normalamount)
        self.amount_label.setStyleSheet("color:white;font-size:14pt;background-color:rgb(51,51,51)")
        
        sendcoinbuttongroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.sendCoinButton = QtWidgets.QPushButton(sendcoinbuttongroupbox)
        self.sendCoinButton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px")
        self.sendCoinButton.setText(self.lang["send_coin"])
        self.sendCoinButton.setGeometry(QtCore.QRect(2, 20, 157, 86))
        self.sendCoinButton.clicked.connect(self.sendCoinScreen)

        
        lockcoinbuttongroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.lockCoinButton = QtWidgets.QPushButton(lockcoinbuttongroupbox)
        self.lockCoinButton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px")
        self.lockCoinButton.setText(self.lang["lock_unlock_amount"])
        self.lockCoinButton.setGeometry(QtCore.QRect(2, 20, 157, 86))
        self.lockCoinButton.clicked.connect(self.lockCoinScreen)

        
        miningbuttongroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.miningButton = QtWidgets.QPushButton(miningbuttongroupbox)
        self.miningButton.setIcon(QtGui.QIcon('pickaxe.png'))
        self.miningButton.setText(self.lang["mining"])
        self.miningButton.setStyleSheet("color:gray;background-color:rgb(31,51,51);font-size:18px")
        self.miningButton.setGeometry(QtCore.QRect(2, 20, 157, 86))
        self.miningButton.clicked.connect(self.miningCoinScreen)

        
        
        myWalletNormalAmount = str(self.myWalletNormalAmount)
        self.myWalletNormalAmountLabel = QtWidgets.QLabel(self.balance2)
        self.myWalletNormalAmountLabel.setText(myWalletNormalAmount)
        self.myWalletNormalAmountLabel.setGeometry(8,27,210,40) 
        self.myWalletNormalAmountLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.myWalletNormalAmountLabel.setStyleSheet("color:white;font-size:14pt;background-color:rgb(51,51,51)")
        
        
        activatedamount = str(self.ActivatedAmount)
        self.activatedamount_label = QtWidgets.QLabel(self.balance3)
        self.activatedamount_label.setText(activatedamount)
        self.activatedamount_label.setGeometry(8,27,210,40) 
        self.activatedamount_label.setAlignment(QtCore.Qt.AlignCenter)
        self.activatedamount_label.setStyleSheet("color:white;font-size:14pt;background-color:rgb(51,51,51)")
        
        
        totallocked = str(self.TotalLockedInLoop)
        self.totallocked_label = QtWidgets.QLabel(self.balance4)
        self.totallocked_label.setText(totallocked)
        self.totallocked_label.setGeometry(8,27,210,40)
        self.totallocked_label.setAlignment(QtCore.Qt.AlignCenter)
        self.totallocked_label.setStyleSheet("color:white;font-size:14pt;background-color:rgb(51,51,51)")
        
        
        self.walletDynamicGroupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)  
        self.walletGroupBoxLayout = QtWidgets.QGridLayout(self.walletDynamicGroupBox)
        
        
        
        self.GridLayout.addWidget(sendcoinbuttongroupbox,5,1,4,5)
        self.GridLayout.addWidget(lockcoinbuttongroupbox,9,1,4,5)
        self.GridLayout.addWidget(miningbuttongroupbox,13,1,4,5)
        
        
        self.GridLayout.addWidget(self.balance1,1,1,3,7)
        self.GridLayout.addWidget(self.balance2,1,8,3,7)
        self.GridLayout.addWidget(self.balance3,1,15,3,7)
        self.GridLayout.addWidget(self.balance4,1,22,3,7)
        
        self.GridLayout.addWidget(self.walletDynamicGroupBox,5,6,12,24)

        
        self.mainInfos()
        

        self.GridLayout.addWidget(self.table,18,1,3,29)
        self.GridLayout.addWidget(QtWidgets.QLabel("\n\n\n\n"),21,0)
        
        

    def button2(self):
        self.clear()
        self.currentMenu("loop")
        
        self.openedLoopsTableFill()
        
        self.closedLoopsTableFill()
        

#        loopRequests.setStyleSheet("color:white;font-size:16px;background-color:rgb(50,100,100);padding:23px;border:1px solid black;")
#        loopRequests.clicked.connect(self.loopRequestsFunc)
        
        sendcoinbuttongroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        sendCoinButton = QtWidgets.QPushButton(sendcoinbuttongroupbox)
        sendCoinButton.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding:15px;")
        sendCoinButton.setText(self.lang["loop_requests_in_loops"]+":"+str(self.loops.requestcount))
        sendCoinButton.setGeometry(QtCore.QRect(2, 20, 164, 86))
        sendCoinButton.clicked.connect(self.loopRequestsFunc)
        
        firstLoopRequestsgroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        firstLoopRequests = QtWidgets.QPushButton(firstLoopRequestsgroupbox)
        firstLoopRequests.setText(self.lang["first_loop_request"])
        firstLoopRequests.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding:15px;")
        firstLoopRequests.clicked.connect(self.firstLoopRequests)
        
        
        checkLoopgroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        checkLoop = QtWidgets.QPushButton(checkLoopgroupbox)
        checkLoop.setText(self.lang["loop_check"])
        checkLoop.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding:15px;")
        checkLoop.clicked.connect(self.checkLoop)
        
        
        loopTransfergroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        loopTransfer = QtWidgets.QPushButton(loopTransfergroupbox)
        loopTransfer.setText(self.lang["loop_transfer"])
        loopTransfer.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding:15px;")
        loopTransfer.clicked.connect(self.loopTransfer)
        
        
        requestLoopgroupbox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        requestLoop = QtWidgets.QPushButton(requestLoopgroupbox)
        requestLoop.setText(self.lang["request_loop"])
        requestLoop.setStyleSheet("color:gray;background-color:rgb(25,51,51);font-size:18px;padding:15px;")
        requestLoop.clicked.connect(self.RequestsLoop)
        
        self.GridLayout.addWidget(sendCoinButton,2,2,1,3)
        self.GridLayout.addWidget(firstLoopRequests,4,2,1,3)
        self.GridLayout.addWidget(checkLoop,6,2,1,3)
        self.GridLayout.addWidget(loopTransfer,8,2,1,3)
        self.GridLayout.addWidget(requestLoop,10,2,1,3)
        
#        self.GridLayout.addWidget(buttonsGroupBox,1,2,12,5)
        
        self.contentManagerGroupBox = QtWidgets.QGroupBox()
        self.contentLayoutManagement = QtWidgets.QGridLayout(self.contentManagerGroupBox)
        self.GridLayout.addWidget(self.contentManagerGroupBox,1,8,12,19)
        
        activeloopstext=QtWidgets.QLabel(self.lang["active_loops"])
        activeloopstext.setStyleSheet("color:white;font-size:13pt;")
        activeloopstext.setFrameShape(QFrame.Panel)
        activeloopstext.setLineWidth(1)
        self.GridLayout.addWidget(activeloopstext,14,2,1,2)
        
        activeloopscount = QtWidgets.QLabel(self.lang["amount"]+":"+str(self.openedloopstable.rowCount()))
        activeloopscount.setStyleSheet("color:white;font-size:13pt")
        activeloopscount.setFrameShape(QFrame.Panel)
        activeloopscount.setLineWidth(1)
        self.GridLayout.addWidget(activeloopscount,14,8,1,2)
        
        activeloopsTotal = QtWidgets.QLabel(self.lang["total_amount"]+":"+str(self.totalAmount))
        activeloopsTotal.setStyleSheet("color:white;font-size:13pt")
        activeloopsTotal.setFrameShape(QFrame.Panel)
        activeloopsTotal.setLineWidth(1)
        self.GridLayout.addWidget(activeloopsTotal,14,11,1,2)
        
        Closedloopstext=QtWidgets.QLabel(self.lang["closed_loops"])
        Closedloopstext.setStyleSheet("color:white;font-size:13pt")
        Closedloopstext.setFrameShape(QFrame.Panel)
        Closedloopstext.setLineWidth(1)
        
        self.GridLayout.addWidget(Closedloopstext,14,15,1,2)
        Closedloopscount = QtWidgets.QLabel(self.lang["amount"]+":"+str(self.closedloopstable.rowCount()))
        Closedloopscount.setStyleSheet("color:white;font-size:13pt")
        Closedloopscount.setFrameShape(QFrame.Panel)
        Closedloopscount.setLineWidth(1)
        
        self.GridLayout.addWidget(Closedloopscount,14,21,1,2)
        ClosedloopsTotal = QtWidgets.QLabel(self.lang["total_amount"]+":"+str(self.totalClosed))
        ClosedloopsTotal.setStyleSheet("color:white;font-size:13pt")
        ClosedloopsTotal.setFrameShape(QFrame.Panel)
        ClosedloopsTotal.setLineWidth(1)
        self.GridLayout.addWidget(ClosedloopsTotal,14,24,1,2)
        
        
        self.GridLayout.addWidget(self.openedloopstable,15,2,6,12)
        self.GridLayout.addWidget(self.closedloopstable,15,15,6,12)
        self.GridLayout.addWidget(QtWidgets.QLabel("\n\n\n\n\n"),22,1)
        
    def button3(self):
        
        self.clear()
        self.currentMenu("Settings")
        
        
        
        self.GridLayout.addWidget(QtWidgets.QLabel(),0,0,3,1)
        
        
        self.privKey = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.privKey.setTitle("Import priv Key") 
        self.privKey.setStyleSheet("QGroupBox::title{color:white;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.privKey.setAlignment(QtCore.Qt.AlignCenter)
        
        dumpPrivkeyEdit = QtWidgets.QLineEdit(self.privKey)
        dumpPrivkeyEdit.setStyleSheet("color:white;margin-top:20px")
        dumpPrivkeyEdit.setGeometry(QtCore.QRect(90, 10, 490, 45))
        
        importButton = QtWidgets.QPushButton(self.privKey)
        importButton.setGeometry(QtCore.QRect(10,30,70,25))
        importButton.setText("Import")
        
        
        self.GridLayout.addWidget(self.privKey,1,3,1,3)
                
        self.bootstrapDownloadQG = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.bootstrapDownloadQG.setTitle(self.bootstrapQGtitle) 
        self.bootstrapDownloadQG.setStyleSheet("QGroupBox::title{color:white;} \n QGroupBox{font:10pt;border: 1px solid gray;margin-top:21px;margin-left:5px;margin-right:1px;}")
        self.bootstrapDownloadQG.setAlignment(QtCore.Qt.AlignCenter)
        
        downloadButton = QtWidgets.QPushButton(self.bootstrapDownloadQG)
        downloadButton.setGeometry(QtCore.QRect(10,35,70,25))
        downloadButton.setText("Download")
        
        
        self.progressBar = QtWidgets.QProgressBar(self.bootstrapDownloadQG)
        self.progressBar.setGeometry(QtCore.QRect(90,30,490,35))
        self.progressBar.setValue(self.bootstrapprogressvalue)
        
        self.__aa = None
        downloadButton.clicked.connect(self.downloadBootStrapF)
        
        self.GridLayout.addWidget(self.bootstrapDownloadQG,2,3,1,3)
        
        
        self.GridLayout.addWidget(QtWidgets.QLabel(),0,5,1,2)
        
        

#        
        self.GridLayout.addWidget(QtWidgets.QLabel(),1,0,8,1)
        
    def downloadBootStrapF(self):
        self.__aa = bootstrap.bootStrapUpdate()
        self.__aa.ssignal.connect(self.updateBootStrapPBar)
        self.__aa.start()
        
        
        
    #if bootstrap download continues it will update progressbar.
    #if download ended end extracting files it will update groupbox title.
    def updateBootStrapPBar(self,val):
        if(val == self.progressbar.value()):
            return
        try:
            try:
                val = int(val)
                self.bootstrapprogressvalue = val
                self.progressBar.setValue(val)
            except:
                if(type(val) != int):
                    self.bootstrapQGtitle = val
                    self.bootstrapDownloadQG.setTitle(val)    
                else:
                    pass
        except:
            pass
            
            
    def __LoopsUpdate(self,liste):
        self.CLOSEDLOOPSDICT = dict(liste[0])
        self.OPENLOOPSDICT = dict(liste[1])
        
        
    def openedLoopsTableFill(self):
        self.openedloopstable = QtWidgets.QTableWidget()
        self.openedloopstable.horizontalHeader().setStretchLastSection(True)
        self.openedloopstable.setColumnCount(1)
        self.openedloopstable.setRowCount(len(self.OPENLOOPSDICT.keys()))
        
        for i in range(len(self.OPENLOOPSDICT.keys())):
            
            pushbutton = QtWidgets.QPushButton()
            pushbutton.setText(str(list(self.OPENLOOPSDICT.keys())[i]))
            pushbutton.clicked.connect(partial(self.__checkLoops,str(list(self.OPENLOOPSDICT.keys())[i]),str(list(self.OPENLOOPSDICT.values())[i])) )
            self.openedloopstable.setCellWidget (i,0,pushbutton)
            
    def __settotalAmount(self,amount):
        
        self.totalAmount = amount
        
    def __settotalClosed(self,amount):
        
        self.totalClosed = amount

        
    def closedLoopsTableFill(self):
        
        self.closedloopstable = QtWidgets.QTableWidget()
        self.closedloopstable.horizontalHeader().setStretchLastSection(True)
        self.closedloopstable.setColumnCount(4)
        self.closedloopstable.setRowCount(len(self.CLOSEDLOOPSDICT.keys()))
        self.closedloopstable.setHorizontalHeaderLabels(["Baton","Miktar","n","Blok"])
        self.closedloopstable.setColumnWidth(0,200)
        self.closedloopstable.setColumnWidth(1,50)
        self.closedloopstable.setColumnWidth(2,50)
        self.closedloopstable.setColumnWidth(3,50)
        for i in range(len(self.CLOSEDLOOPSDICT.keys())):
            pushbutton = QtWidgets.QPushButton()
            pushbutton.setText(str(list(self.CLOSEDLOOPSDICT.keys())[i])[0:30])
            pushbutton.clicked.connect(partial(self.__checkLoops,str(list(self.CLOSEDLOOPSDICT.keys())[i]),str(list(self.CLOSEDLOOPSDICT.values())[i])) )
            x = ast.literal_eval(str(list(self.CLOSEDLOOPSDICT.values())[i]))
            self.closedloopstable.setCellWidget(i,0,pushbutton)
            self.closedloopstable.setItem(i,1,QTableWidgetItem(str(x["collected"])))
            self.closedloopstable.setItem(i,2,QTableWidgetItem(str(x["n"])))
            self.closedloopstable.setItem(i,3,QTableWidgetItem(str(x["height"])))
            
        self.closedloopstable.update()
    def __checkLoops(self,txid,value):
        
        self.clearContentScreen()
        x = ast.literal_eval(value)
        
        try:
            _settlement = x["settlement"]
        except:
            pass
        _createtxid = x["createtxid"]
        _height = x["height"]
        _currency = x["currency"]
        _funcid = x["funcid"]
        _amount = x["collected"]
        
        
        
        txidLabel = QtWidgets.QLabel("Baton:"+txid)
        txidLabel.setAlignment(QtCore.Qt.AlignCenter)
        txidLabel.setStyleSheet("color:rgb(220,220,220);font-size:10pt;margin:20px")
        txidLabel.setFrameShape(QFrame.Panel)
        txidLabel.setMaximumWidth(600)
        self.contentLayoutManagement.addWidget(txidLabel,0,0,1,4)
        
        
        heightLabel = QtWidgets.QLabel("Blok:"+str(_height))
        heightLabel.setAlignment(QtCore.Qt.AlignCenter)
        heightLabel.setStyleSheet("color:rgb(220,220,220);font-size:10pt;margin:20px")
        heightLabel.setFrameShape(QFrame.Panel)
        heightLabel.setMaximumWidth(200)
        self.contentLayoutManagement.addWidget(heightLabel,1,0,1,2)
        
        
        currencyLabel = QtWidgets.QLabel("Coin Birimi:"+str(_currency))
        currencyLabel.setAlignment(QtCore.Qt.AlignCenter)
        currencyLabel.setStyleSheet("color:rgb(220,220,220);font-size:10pt;margin:20px")
        currencyLabel.setFrameShape(QFrame.Panel)
        currencyLabel.setMaximumWidth(200)
        self.contentLayoutManagement.addWidget(currencyLabel,1,2,1,2)
        
        funcidLabel = QtWidgets.QLabel("Func id:"+str(_funcid))
        funcidLabel.setAlignment(QtCore.Qt.AlignCenter)
        funcidLabel.setStyleSheet("color:rgb(220,220,220);font-size:10pt;margin:20px")
        funcidLabel.setFrameShape(QFrame.Panel)
        funcidLabel.setMaximumWidth(200)
        self.contentLayoutManagement.addWidget(funcidLabel,2,0,1,2)
        
        amountLabel = QtWidgets.QLabel("Miktar:"+str(_amount))
        amountLabel.setAlignment(QtCore.Qt.AlignCenter)
        amountLabel.setStyleSheet("color:rgb(220,220,220);font-size:10pt;margin:20px;")
        amountLabel.setFrameShape(QFrame.Panel)
        amountLabel.setMaximumWidth(200)
        self.contentLayoutManagement.addWidget(amountLabel,2,2,1,2)
        
        
        settleLabel = QtWidgets.QLabel("Aktarılan Hesap:"+str(_settlement))
        settleLabel.setAlignment(QtCore.Qt.AlignCenter)
        settleLabel.setStyleSheet("color:rgb(220,220,220);font-size:10pt;margin:20px")
        settleLabel.setFrameShape(QFrame.Panel)
        settleLabel.setMaximumWidth(600)
        self.contentLayoutManagement.addWidget(settleLabel,3,0,1,4)
        
        
        createTxid = QtWidgets.QLabel("Create Txid:"+str(_createtxid))
        createTxid.setAlignment(QtCore.Qt.AlignCenter)
        createTxid.setStyleSheet("color:rgb(220,220,220);font-size:10pt;margin:20px")
        createTxid.setFrameShape(QFrame.Panel)
        createTxid.setMaximumWidth(600)
        self.contentLayoutManagement.addWidget(createTxid,4,0,1,4)
        

        

        
        self.contentLayoutManagement.update()
    def loopRequestsFunc(self, event):
        
        self.clearContentScreen()
        
        table = QtWidgets.QTableWidget()
        table.horizontalHeader().setStretchLastSection(True)
        try:
            self.requestsList
        except:
            return
        table.setRowCount(len(self.requestsList))
        table.setColumnCount(1)
        for i in range(len(self.requestsList)):
            
            pushbutton = QtWidgets.QPushButton()
            pushbutton.setText(str(self.requestsList[i]["txid"]))
            pushbutton.clicked.connect(partial(self.clickedLoopRequests,self.requestsList[i]))
            table.setCellWidget(i,0,pushbutton)
        
        table.update()
        
        self.contentLayoutManagement.addWidget(table,0,0)
        self.contentLayoutManagement.update()
    def clickedLoopRequests(self,infoList):
        self.clearContentScreen()
        
        txidlabel = QtWidgets.QLabel("Baton:"+infoList["txid"])        
        txidlabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
        amountLabel = QtWidgets.QLabel(self.lang["amount"]+":"+str(infoList["amount"]))
        amountLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
        maturesLabel = QtWidgets.QLabel(self.lang["matures"]+":"+str(infoList["matures"]))
        maturesLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
        receivepkLabel = QtWidgets.QLabel(self.lang["receive_pubkey"]+":"+str(infoList["receivepk"]))
        receivepkLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
        
        self.contentLayoutManagement.addWidget(txidlabel,0,0,1,5)
        self.contentLayoutManagement.addWidget(amountLabel,1,0,1,5)
        self.contentLayoutManagement.addWidget(maturesLabel,2,0,1,5)
        self.contentLayoutManagement.addWidget(receivepkLabel,3,0,1,5)
        
        acceptButton = QtWidgets.QPushButton(self.contentManagerGroupBox)
        acceptButton.setText(self.lang["confirm"])
        acceptButton.clicked.connect(partial(self.__threadCaller,infoList["txid"],infoList["receivepk"]))
        
        self.contentLayoutManagement.addWidget(acceptButton,4,2)
        
        
    def updateRequests(self,liste):
        self.requestsList = liste
        
    def __threadCaller(self,txid,receiverpk):
        Thread(target=self.acceptLoop, args=(txid, receiverpk)).start()
        self.clearContentScreen()
        
    def acceptLoop(self,txid,receiverpk):
        x = subprocess.run("komodo-cli -ac_name=MCL marmaraissue "+receiverpk+' \"{\\"avalcount\\":\\"n\\", \\"autosettlement\\":\\"true\\"|\\"false\\", \\"autoinsurance\\":\\"true\\"|\\"false\\", \\"disputeexpires\\":\\"offset\\", \\"EscrowOn\\":\\"true\\"|\\"false\\", \\"BlockageAmount\\":\\"amount\\" }\" '+ txid,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        _json = str(x.stdout)[2:-5]
        _json = _json.replace("\\r","")
        _json = _json.replace("\\n","")
        
        _json = json.loads(_json)
        
        subprocess.run("komodo-cli -ac_name=MCL sendrawtransaction "+_json["hex"],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        
        
        
    def firstLoopRequests(self, event):
        self.clearContentScreen()
        
        receiverpklabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        receiverpklabel.setText(self.lang["pubkey_address"]) 
        receiverpklabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(receiverpklabel,0,0)
        
        self.receiverpkText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.contentLayoutManagement.addWidget(self.receiverpkText,0,1,1,5)
        
        amountlabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        amountlabel.setText(self.lang["amount_pubkey_requests"])
        amountlabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(amountlabel,1,0)
        
        self.LoopRequestamountText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.contentLayoutManagement.addWidget(self.LoopRequestamountText,1,1,1,5)
        
        maturesLabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        maturesLabel.setText(self.lang["matures_on_first_pubkey_requests"])
        maturesLabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(maturesLabel,2,0)
        
        self.loopRequestmaturesText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.contentLayoutManagement.addWidget(self.loopRequestmaturesText,2,1,1,5)
        
        sendButton = QtWidgets.QPushButton(self.contentManagerGroupBox)
        sendButton.setText(self.lang["send"])
        sendButton.clicked.connect(self.firstLoopRequestCommand)
        self.contentLayoutManagement.addWidget(sendButton,4,2)
        
        
        self.contentLayoutManagement.update()
        
    def firstLoopRequestCommand(self):
        pubkey = self.receiverpkText.text()
        amount = self.LoopRequestamountText.text()
        matures = self.loopRequestmaturesText.text()
        self.clearContentScreen()
        waitingLabel = QtWidgets.QLabel(self.lang["request_sending"])
        waitingLabel.setAlignment(QtCore.Qt.AlignCenter)
        waitingLabel.setStyleSheet("font-size:20pt;color:white")
        self.contentLayoutManagement.addWidget(waitingLabel,0,0)
        self.contentLayoutManagement.update() 
#        Thread(target=self.__firstLoopRequestCommand, args=(pubkey, amount,matures)).start()
        self.__firstLoopRequestCommand(pubkey,amount,matures)
        
    def __firstLoopRequestCommand(self,pubkey,amount,matures):
        x = subprocess.run("komodo-cli -ac_name=MCL marmarareceive "+pubkey+" "+amount+" MARMARA "+ matures +' \"{\\"avalcount\\":\\"n\\"}\" ',  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        try:
            _json = str(x.stdout)[2:-5]
            _json = _json.replace("\\r","")
            _json = _json.replace("\\n","")
            
            _json = json.loads(_json)
            
            xbaton = subprocess.run("komodo-cli -ac_name=MCL sendrawtransaction "+_json["hex"],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            
            
            baton = str(xbaton.stdout)[2:-5]
            baton = baton.replace("\\r","")
            baton = baton.replace("\\n","")
            
            
            self.clearContentScreen()
            lengthofbaton = len(baton)
            if(lengthofbaton>20):
                baton = baton[0:20] +"\n"+baton[20:-1]
                lengthofbaton -= 20
                
            waitingLabel = QtWidgets.QLabel(self.lang["request_succeded_and_baton"]+":"+baton)
            waitingLabel.setAlignment(QtCore.Qt.AlignCenter)
            waitingLabel.setStyleSheet("font-size:15pt;color:white")
            self.contentLayoutManagement.addWidget(waitingLabel,0,0)
            self.contentLayoutManagement.update() 
        except Exception as e:
            self.clearContentScreen()
            waitingLabel = QtWidgets.QLabel(self.lang["request_failed"]+str(e.args))
            waitingLabel.setAlignment(QtCore.Qt.AlignCenter)
            waitingLabel.setStyleSheet("font-size:20pt;color:white")
            self.contentLayoutManagement.addWidget(waitingLabel,0,0)
            self.contentLayoutManagement.update() 
        
    def checkLoop(self, event):
        self.clearContentScreen()
        txidLabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        txidLabel.setText(self.lang["enter_baton_in_check_loop"])
        txidLabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(txidLabel,0,0,1,1)
        
        self.checkLooptxidText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.contentLayoutManagement.addWidget(self.checkLooptxidText,0,1,1,5)
        
        checkButton = QtWidgets.QPushButton(self.contentManagerGroupBox)
        checkButton.setText(self.lang["check_button_in_check_loop"])
        checkButton.clicked.connect(self.checkloopCommand)
        self.contentLayoutManagement.addWidget(checkButton,3,2)
        
        self.contentLayoutManagement.update()
        
    def checkloopCommand(self,txid=""):
        looper = LoopControlThread()
        looper.loopssignal.connect(self.__checkLoopCommand)
        try:
            looper.setTxid(self.checkLooptxidText.text())
        except:
            looper.setTxid(txid)
        looper.start()
        
        self.clearContentScreen()
        waitingLabel = QtWidgets.QLabel(self.lang["loading_in_check_loop"])
        waitingLabel.setAlignment(QtCore.Qt.AlignCenter)
        waitingLabel.setStyleSheet("font-size:30pt;color:white")
        self.contentLayoutManagement.addWidget(waitingLabel,0,0)
        self.contentLayoutManagement.update() 
        
    def __checkLoopCommand(self,x):
        
        
        
        _json = str(x.stdout)[2:-5]
        _json = _json.replace("\\r","")
        _json = _json.replace("\\n","")
        try:
            _json = json.loads(_json)
        
            self.clearContentScreen()
            
            createtxidLabel = QtWidgets.QLabel("Baton:"+_json["createtxid"])
            createtxidLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
            self.contentLayoutManagement.addWidget(createtxidLabel,0,0)
            try:
                issuerpkLabel = QtWidgets.QLabel("Pubkey:"+_json["pubkey"])
                issuerpkLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
                self.contentLayoutManagement.addWidget(issuerpkLabel,1,0)
            except:
                issuerpkLabel = QtWidgets.QLabel("issuerpk:"+_json["issuerpk"])
                issuerpkLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
                self.contentLayoutManagement.addWidget(issuerpkLabel,1,0)
            try:
                amountLabel = QtWidgets.QLabel("Miktar:"+str(_json["amount"]))
                amountLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
                self.contentLayoutManagement.addWidget(amountLabel,2,0)
            except:
                amountLabel = QtWidgets.QLabel("Miktar:"+str(_json["collected"]))
                amountLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
                self.contentLayoutManagement.addWidget(amountLabel,2,0)
            try:
                maturesLabel = QtWidgets.QLabel("Blok:"+str(_json["matures"]))
                maturesLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
                self.contentLayoutManagement.addWidget(maturesLabel,3,0)
            except:
                maturesLabel = QtWidgets.QLabel("Süre:"+str(_json["height"]))
                maturesLabel.setStyleSheet("color:rgb(220,220,220);font-size:11pt")
                self.contentLayoutManagement.addWidget(maturesLabel,3,0)
                
            self.contentLayoutManagement.update()
            

            
            
        except Exception as e:
            self.clearContentScreen()
            waitingLabel = QtWidgets.QLabel("Hata gerçekleşti."+str(e.args))
            waitingLabel.setAlignment(QtCore.Qt.AlignCenter)
            waitingLabel.setStyleSheet("font-size:20pt;color:white")
            self.contentLayoutManagement.addWidget(waitingLabel,0,0)
            self.contentLayoutManagement.update() 
        
    def loopTransfer(self, event):
        self.clearContentScreen()
        receiverpkLabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        receiverpkLabel.setText(self.lang["receive_pubkey_in_loop_transfer"]+" ")
        receiverpkLabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(receiverpkLabel,0,0,1,1)
        
        self.TransferreceiverpkText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.contentLayoutManagement.addWidget(self.TransferreceiverpkText ,0,1,1,5)
        
        batonLabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        batonLabel.setText(self.lang["baton_in_loop_transfer"]+" ")
        batonLabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(batonLabel,1,0,1,1)
        
        self.TransferbatonText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.contentLayoutManagement.addWidget(self.TransferbatonText ,1,1,1,5)
        
        sendButton = QtWidgets.QPushButton(self.contentManagerGroupBox)
        sendButton.setText(self.lang["transfer_button_in_loop_transfer"])
        sendButton.clicked.connect(self.loopTransferCommand)
        self.contentLayoutManagement.addWidget(sendButton,3,2)
        
        self.contentLayoutManagement.update()
        
    def loopTransferCommand(self):
        receiverpk=self.TransferreceiverpkText.text()
        requesttxid = self.TransferbatonText.text()
        Thread(target=self.__loopTransferCommand,args=(receiverpk,requesttxid)).start()
        
    def __loopTransferCommand(self,receiverpk,requesttxid):
        
        x = subprocess.run("komodo-cli -ac_name=MCL marmaratransfer "+receiverpk+' \"{\\"avalcount\\":\\"n\\"}\" '+requesttxid, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        
        _json = str(x.stdout)[2:-5]
        _json = _json.replace("\\r","")
        _json = _json.replace("\\n","")
        
        _json = json.loads(_json)
        
        subprocess.run("komodo-cli -ac_name=MCL sendrawtransaction "+_json["hex"],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        
        
    def RequestsLoop(self, event):
        self.clearContentScreen()
        
        senderpkLabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        senderpkLabel.setText(self.lang["sender_pubkey_loop_requests"])
        senderpkLabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(senderpkLabel,0,0,1,1)
        
        self.ReceivesenderpkText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.ReceivesenderpkText.setStyleSheet("color:white")
        self.contentLayoutManagement.addWidget(self.ReceivesenderpkText ,0,1,1,5)

        txidLabel = QtWidgets.QLabel(self.contentManagerGroupBox)
        txidLabel.setText(self.lang["baton_in_loop_requests"])
        txidLabel.setStyleSheet("color:white;font-size:13pt")
        self.contentLayoutManagement.addWidget(txidLabel,1,0,1,1)
        
        self.ReceivetxidText = QtWidgets.QLineEdit(self.contentManagerGroupBox)
        self.ReceivetxidText.setStyleSheet("color:white")
        self.contentLayoutManagement.addWidget(self.ReceivetxidText ,1,1,1,5)
        
        requestButton = QtWidgets.QPushButton(self.contentManagerGroupBox)
        requestButton.setText(self.lang["send_requests_button_in_loop_requests"])
        requestButton.clicked.connect(self.RequestsLoopCommand)
        self.contentLayoutManagement.addWidget(requestButton,3,2)

        self.contentLayoutManagement.update()
    
    def RequestsLoopCommand(self):
        pubkey = self.ReceivesenderpkText.text()
        txid = self.ReceivetxidText.text()
        Thread(target=self.__RequestsLoopCommand,args=(pubkey,txid))
    
    def __RequestsLoopCommand(self,pubkey,txid):
        
        x = subprocess.run("komodo-cli -ac_name=MCL marmarareceive "+ pubkey +" "+ txid+' \"{\\"avalcount\\":\\"n\\"}\" ',  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        
        _json = str(x.stdout)[2:-5]
        _json = _json.replace("\\r","")
        _json = _json.replace("\\n","")
        
        _json = json.loads(_json)
        
        subprocess.run("komodo-cli -ac_name=MCL sendrawtransaction "+_json["hex"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        
    
    def history_tab(self):
        
        self.table = QtWidgets.QTableWidget()
        self.table.updatesEnabled()
        self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.setGeometry(0, 300, 200,50)
        self.table.setColumnCount(4)
        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,100)
        self.table.setHorizontalHeaderLabels([self.lang["date"],self.lang["type"],self.lang["net_change"],self.lang["txid"]])
        try:
            self.__hist
        except:
            self.__hist = []
        while(self.__hist is None):
            time.sleep(0.25)
        if(len(self.__hist) == 0):
            self.table.setRowCount(1)
            self.table.setItem(0,0,QTableWidgetItem("loading..."))
            self.table.setItem(0,1,QTableWidgetItem("loading..."))
            self.table.setItem(0,2,QTableWidgetItem("loading..."))
            
            
        for i in range(len(self.__hist)):
            
            
            if(len(self.__hist)>10):    
                self.table.setRowCount(len(self.__hist))
            else:
                self.table.setRowCount(10)
            
            
            pushbutton = QtWidgets.QPushButton(self.table)
            pushbutton.setText(self.__hist[i]["Txid"])
            pushbutton.clicked.connect(partial(self.open_link,self.__hist[i]["Txid"]))
            
            self.table.setItem(i,0,QTableWidgetItem(self.__hist[i]["time"]))
            self.table.setItem(i,1,QTableWidgetItem(self.__hist[i]["type"]))
            self.table.setItem(i,2,QTableWidgetItem(self.__hist[i]["Node balance"]))
            self.table.setCellWidget (i,3,pushbutton)
            
        self.table.update()
        self.GridLayout.update()
        self.gridLayoutWidget.update()
        self.centralwidget.update()
    def newHistory(self,liste = []):
        try:
            if(self.__hist != liste):
                self.__hist = liste
                if(self.currentOpenedMenu == "wallet"):
                    self.button1()
        except:
            time.sleep(3)
            pass
        self.__hist = liste
        self.history_tab()
        
    def currentMenu(self,menuname):
        self.currentOpenedMenu = menuname
        



    def open_link(self,txid):
        link = "http://explorer.marmara.io/tx/" + txid
        webbrowser.open(link)
        
    
        
        
    def get_balance(self):
        self.normalamount = "connecting..."
        
        self.ActivatedAmount="connecting..."   #kilitli bakiye
        
        self.TotalLockedInLoop="connecting..." 
        
        self.myWalletNormalAmount = "connecting..."
        
        while not self.stop:
            try:
                x = subprocess.run("komodo-cli -ac_name=MCL marmarainfo 0 0 0 0 "+self.__pubkey,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                
                _json = str(x.stdout)[2:-5]
                _json = _json.replace("\\r","")
                _json = _json.replace("\\n","")

                try:
                    _json = json.loads(_json)
                    
                    self.normalamount = str(round(_json["myPubkeyNormalAmount"],2))
                    
                    self.ActivatedAmount=str(round(_json["myActivatedAmount"],2))   #kilitli bakiye
                    
                    self.TotalLockedInLoop=str(round(_json["TotalLockedInLoop"],2))     #Lcl bakiye
                    
                    self.myWalletNormalAmount=str(round(_json["myWalletNormalAmount"],2))
                    
                    
                    self.activeLoops = str(_json["issuances"])[0:3]
                    
                    self.closedLoops = str(_json["closed"])[0:3]
                    
                except Exception as e:
                    if("list index out of range" in e):
                        pass
                    else:
                        pass
                    self.normalamount = "connecting..."
                    
                    self.ActivatedAmount="connecting..."   #kilitli bakiye
                    
                    self.TotalLockedInLoop="connecting..." 
                    
                    self.myWalletNormalAmount = "connecting..."
                    
                    
                    self.activeLoops = []
                    self.closedLoops = []
                    
                    time.sleep(0.25)
                    self.amount_label.update()
                    self.activatedamount_label.update()
                    self.totallocked_label.update()
                    self.normalAddressAmount.update()
                    self.myWalletNormalAmountLabel.update()

                time.sleep(1)
                self.amount_label.setText(self.normalamount)
                self.activatedamount_label.setText(self.ActivatedAmount)
                self.totallocked_label.setText(self.TotalLockedInLoop)
                self.myWalletNormalAmountLabel.setText(self.myWalletNormalAmount)
                
                
                self.myWalletNormalAmountLabel.update()
                self.amount_label.update()
                self.activatedamount_label.update()
                self.totallocked_label.update()
                
                
            except:
                time.sleep(0.5)
                continue
            
    def copyAddressToClipboard(self,event):
        pyperclip.copy(self.__walletaddress)
        
    def copyPubkeyToClipboard(self,event):
        pyperclip.copy(self.__pubkey)
        
    def CloseChain(self):
        subprocess.run("komodo-cli.exe -ac_name=MCL stop",  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    def closeEvent(self, Event):
        self.stop = True
        self.miningstatus.stopThread()
        self.Threader.stopThread()
        self.historyAgent.stopThread()
        self.loops.stopThread()
        self.loopTables.stopper()
        Thread(target=self.CloseChain).start()
        time.sleep(0.5)
        QtWidgets.QApplication.quit
        self.destroy()
        raise KeyError 
            
            
