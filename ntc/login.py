import tkinter
from PyQt5.QtWidgets import *
import subprocess,sys


from PyQt5.QtCore import *
import os
import time
import json
import shutil
import zipfile
import datetime
import sidebaar
from threading import Thread
import loginui
from PyQt5 import QtCore, QtGui, QtWidgets

import langsupport

#
SYSTEM_ENVIRONMENT_WORKPLACE = 'APPDATA'

class newprofilewindow(object):
    lang = ""
    def setLang(self,lang):
        self.lang = lang
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(313, 284)
        Dialog.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 110, 171, 31))
        self.label.setStyleSheet("font: 10pt \"Comic Sans MS\";")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(60, 160, 211, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 200, 81, 31))
        self.pushButton.setStyleSheet("background-color:  #6c7585; color:#ebdeb1;font: 10pt \\\"Comic Sans MS\\\";")
        self.pushButton.setObjectName("pushButton")


        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(120, 0, 280, 100))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        pixmap = QtGui.QPixmap("icon.png")
        self.label_2.setPixmap(pixmap)


        Dialog.setWindowTitle(self.lang["create_new_profile"])
        self.label.setText(self.lang["enter_name_for_new_profile"])
        self.pushButton.setText(self.lang["create"])


        QtCore.QMetaObject.connectSlotsByName(Dialog)


class importWalletWindow(object):
    lang = ""
    def setLang(self,lang):
        self.lang = lang
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(538, 466)
        Dialog.setStyleSheet("background-color: rgb(240, 240, 240)")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 140, 141, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 190, 141, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 240, 141, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 290, 141, 31))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(160, 140, 311, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 190, 311, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 240, 311, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 290, 311, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(360, 330, 111, 23))
        self.pushButton.setStyleSheet("background-color:  #6c7585; color:#ebdeb1;font: 10pt\"Comic Sans MS\"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 390, 131, 31))
        self.pushButton_2.setStyleSheet("background-color:  #6c7585; color:#ebdeb1;font: 10pt\"Comic Sans MS\"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(100, 430, 391, 20))
        self.label_5.setStyleSheet("color: rgb(170, 0, 0);")
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(250,20, 280, 100))
        self.label_6.setText("")
        self.label_6.setObjectName("label_2")
        pixmap = QtGui.QPixmap("icon.png")
        self.label_6.setPixmap(pixmap)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        _translate = QtCore.QCoreApplication.translate
        
        Dialog.setWindowTitle(self.lang["load_wallet"])
        self.label.setText(self.lang["enter_name_for_new_profile"])
        self.label_2.setText(self.lang["enter_name_for_backup"])
        self.label_3.setText(self.lang["enter_wallet_pubkey"])
        self.label_4.setText(self.lang["wallet_file_path"])
        self.pushButton.setText(self.lang["open_wallet"])
        self.pushButton_2.setText(self.lang["load"])
        self.label_5.setText(self.lang["wrong_pubkey_warning"])

#called when loading a wallet(wallet.dat)
class ThreadofLoadWallet(QtCore.QThread):
    ssignal = QtCore.pyqtSignal(object)
    def __init__(self,pubkey):
        self.pubkey=pubkey
        QtCore.QThread.__init__(self)
    def run(self):
        try:
            while True:
                try:
                    x = subprocess.run("komodo-cli -ac_name=MCL marmarainfo 0 0 0 0 "+self.pubkey, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
#                    print(x)
                    if(str(x.stdout) != "b''"): 
                        output = str(x.stdout)
                        subprocess.run("komodo-cli -ac_name=MCL stop", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                        self.ssignal.emit(output)
                        break
                except:
                    continue
        except:
            pass
            
#called when creating new address
class ControlThread(QtCore.QThread):

    loopssignal = QtCore.pyqtSignal(object)
    startchainagainsignal = QtCore.pyqtSignal(object)
    blockcount = 0
    wallet_adress = ""
    pubkey = ""
    priv_key = ""
    def __init__(self):
        QtCore.QThread.__init__(self)

    def emitter(self):
        self.loopssignal.emit([self.wallet_adress,self.pubkey,self.priv_key])

    def run(self):
        self.process()

    def process(self):
        count = 2
        while True:
            if(count < 0 and count%2 == 0):
                self.startchainagainsignal.emit([ ])
            self.wallet_adress = subprocess.run("komodo-cli.exe -ac_name=MCL getnewaddress", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)  
            self.wallet_adress = str(self.wallet_adress.stdout)[2:-5]
            self.pubkey = subprocess.run("komodo-cli.exe -ac_name=MCL validateaddress "+self.wallet_adress, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True) 
            self.pubkey = str(self.pubkey.stdout)[2:-5]
            self.pubkey = self.pubkey.replace("\\r\\n","")
            time.sleep(1)
            self.priv_key = subprocess.run("komodo-cli.exe -ac_name=MCL dumpprivkey "+self.wallet_adress, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            self.priv_key = str(self.priv_key.stdout)[2:-5]
            if(self.wallet_adress == "" or self.pubkey == "" or self.priv_key == "" or "error" in self.wallet_adress or "error" in self.pubkey or "error" in self.priv_key):
                count -=1
                continue
            else:
                self.emitter()
                break

#creating new account(also new address) ui and all other things...
class newAccount(QMainWindow):     
    refreshcombobox = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(newAccount, self).__init__(parent)
        self.setFixedSize(600,450)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 600, 450))
        
        self.gridlayout = QtWidgets.QGridLayout(self.centralwidget)
        
        self.setCentralWidget(self.centralwidget)
        self.button = QtWidgets.QPushButton()
    def controller(self):
        try:
            self.profileName = self.dialog_window.lineEdit.text()
            self.dialog.destroy()
            Thread(target=self.start_chain_without_pubkey).start()
            waitingLabel = QtWidgets.QLabel("Zincire bağlanılıyor...")
            waitingLabel.setAlignment(QtCore.Qt.AlignCenter)
            waitingLabel.setStyleSheet("font-size:30pt")
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            
            self.gridlayout.addWidget(waitingLabel,0,0)
            self.gridlayout.update()
            
            
            self.threader = ControlThread()
            self.threader.loopssignal.connect(self.save_new_wallet)
            self.threader.startchainagainsignal.connect(lambda:Thread(target=self.start_chain_without_pubkey).start())
            self.threader.start()
            self.show()
        except:
            pass
    def _create_new_account(self,lang):
        try:
            self.dialog = QtWidgets.QDialog(self)
            self.dialog_window = newprofilewindow()
            self.dialog_window.setLang(lang)
            self.dialog_window.setupUi(self.dialog)
            
            self.dialog_window.pushButton.clicked.connect(self.controller)
            self.dialog.exec_()
        except:
            pass
        
    def save_new_wallet(self,liste):

        wallet_address = liste[0]
        pubkey = liste[1]
        priv_key = liste[2]
        

        x = QtWidgets.QFileDialog.getExistingDirectory()
        with open(x+r"/"+self.profileName+".txt","w") as f:
            pubkey = pubkey.replace("'",'"')
            pubkey = pubkey.replace(" ","")
            dictionary_pubkey = dict(json.loads(pubkey))
            dictionary = {priv_key:dict(dictionary_pubkey)}
            f.write(json.dumps(dictionary,indent=4))
       
        self.add_profile(self.profileName,pubkey)
        subprocess.run("komodo-cli.exe -ac_name=MCL stop", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        self.destroy()
        self.refreshcombobox.emit()
    def clearScreen(self):
        layout = self.gridlayout
        while layout.count():
            child = layout.takeAt(0)
            child.widget().deleteLater()
            del child
        
    def add_profile(self,profile_name,pubkey):
        try:
            with open("walletProfiles.txt","r") as f:
                pass
        except:
            with open("walletProfiles.txt","w") as f:
                pass
        with open("walletProfiles.txt","r") as f:
            text = f.read()
            if(text != ""):
                _json = text.replace("'",'"')
                
                
                dictionary = dict()
                
                dictionary = json.loads(_json)
                
                dictionary_pubkey = dict(json.loads(pubkey))
                
                dictionary[profile_name] = dictionary_pubkey
                with open("walletProfiles.txt","w") as x:
                    x.write(json.dumps(dictionary,indent=4))
            else:
                _json = pubkey.replace('"',"")
                with open("walletProfiles.txt","a") as z:
                    json.dump(json.loads('{"'+profile_name+'":'+pubkey+'}'),z,indent=4)
    
        
    def start_chain_without_pubkey(self):
        self.chain = subprocess.run("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

#starter class
class _login():
    def stopper(self):
        subprocess.run("komodo-cli.exe -ac_name=MCL stop", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    def __init__(self):
        
        Thread(target=self.stopper).start()
        path = os.getenv(SYSTEM_ENVIRONMENT_WORKPLACE)
        
        
        
        try:
            os.chdir(path+r"\Komodo\MCL\Application Data")
        except:
            os.mkdir(path+r"\Komodo\MCL\Application Data")
            os.chdir(path+r"\Komodo\MCL\Application Data")
        
        if("cfg.txt" not in os.listdir()):
            with open("cfg.txt","w") as f:
                f.write("{")
                f.writelines("\"language\":\"en\"")
                f.write("}")
        with open("cfg.txt","r") as f:
            self.language_in_config= dict(json.loads(f.read()))["language"]
        langsupport.downloadLanguages()
        self.LANG = langsupport.language(self.language_in_config,os.getcwd()).LANG
        

        if "walletProfiles.txt" not in os.listdir():
            with open("walletProfiles.txt","w") as f:
                f.write("{}")
        #very starting screen, if files are full in zcash, this screen pass very fast.
        self.downloading_screen = tkinter.Tk()
        self.downloading_screen.attributes("-topmost", True)
        self.downloading_screen.overrideredirect(True)
        self.downloading_screen.geometry("200x200+900+400")
        
        self.Login()
        self.downloading_screen.mainloop()
        
        self.actualy_login()
        
    #check if required files are exist. If not run fetch-params
    def Login(self):
        self.label2 = tkinter.Label(self.downloading_screen,text="\n\n\n\n\n")
        self.label2.grid(row=0,column=0)
        self.label3 = tkinter.Label(self.downloading_screen,text="            ")
        self.label3.grid(row=1,column=0)
        self.label = tkinter.Label(self.downloading_screen,text="Checking files...")
        self.label.grid(row=1,column=1)
        self.label.update()
        #Check if file is missing
        path = os.getenv(SYSTEM_ENVIRONMENT_WORKPLACE) + "\ZcashParams"
        if os.path.exists(path):
            files = os.listdir(path)
            check_list = ["sapling-output.params","sapling-spend.params","sprout-groth16.params","sprout-proving.key","sprout-verifying.key"]
            download = False
            for i in check_list:
                self.label.configure(text="checking "+str(i))
                self.label.update()
                if i not in files:
                    download = True
        else:
            download = True
        #if any of file is missing, download will be true so we run fetch-params
        if(download):
            self.label.configure(text="We are downloading\n   missing files...")
            self.label.update()
            x = (subprocess.run("fetch-params.bat", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True))
            if("saved" in str(x.stderr)):
                self.label.configure(text="Completed!")
                self.label.update
            else:
                self.label.configure(text="An error occurred during downloading")
                self.label.update()
        else:
            self.label.configure(text="All required files checked!\n Program starting")
            self.label.update()
        self.downloading_screen.destroy()
        
    def actualy_login(self):
        
        #login main page
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.setWindowTitle("EasyGUI for MCL")
        self.ui = loginui.Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        
        
        
        try:
            self.ui.comboBox.addItems(self.read_profiles())
        except:
            self.ui.comboBox.addItems([])
        
        self.new_account = newAccount()
        self.new_account.refreshcombobox.connect(self.update_profilescombobox)
        
        
        
        self.ui.pushButton.clicked.connect(self.open_wallet_completely)
        self.ui.pushButton_2.clicked.connect(lambda x:self.new_account._create_new_account(self.LANG))
        self.ui.pushButton_3.clicked.connect(self.importwallet)
        self.ui.pushButton_4.clicked.connect(self.loadbackup)
        
        
        self.ui.pushButton_3.setText(self.LANG["load_wallet"])
        self.ui.pushButton_4.setText(self.LANG["Load_from_backup"])
        self.ui.label.setText(self.LANG["login"])
        self.ui.pushButton.setText(self.LANG["login"])
        self.ui.pushButton_2.setText(self.LANG["create_new_profile"])
        self.ui.label_4.setText(self.LANG["language"]+":")
        self.ui.comboBox_2.addItems(langsupport.language_list())
        
        self.ui.comboBox_2.setCurrentText(self.language_in_config) 
        self.ui.comboBox_2.currentIndexChanged.connect(lambda x:langsupport.change_language_value(self.ui.comboBox_2,self.MainWindow,self.LANG))
    

        
        self.MainWindow.show()
        sys.exit(self.app.exec_())
        
        
        
        
    def update_profilescombobox(self):
        #when we make changes over profiles, update combobox to show last form of profiles.
        self.ui.comboBox.clear()
  
        self.ui.comboBox.addItems(self.read_profiles())
        
    #read profiles from file in json format and return them as a list.
    def read_profiles(self):
        with open("walletProfiles.txt","r") as f:
            text = f.read()
            _json = dict(json.loads(text))
        profile_list = list()
        for i in _json.keys():
            profile_list.append(i)
        return profile_list
        
    #import wallet screen ui and all other things.
    def importwallet(self):
        try:
            self.dialog = QtWidgets.QDialog()
            self.dialog_window = importWalletWindow()
            self.dialog_window.setLang(self.LANG)
            self.dialog_window.setupUi(self.dialog)
            self.dialog_window.pushButton.clicked.connect(lambda:self.dialog_window.lineEdit_4.setText(str(QtWidgets.QFileDialog.getOpenFileName())[2:-19]))
            self.dialog_window.pushButton_2.clicked.connect(self.backup_import)
            self.dialog.exec_()
        except Exception as e:
            print(e.args)
            pass
    def backup_import(self):
        try:
            name = self.dialog_window.lineEdit_2.text()
            path = os.getenv(SYSTEM_ENVIRONMENT_WORKPLACE)
            
            os.chdir(path+r"\Komodo\MCL\Application Data")
            try:
                os.mkdir("backups")
            except:
                pass
            
            with zipfile.ZipFile(".\\backups\\"+name+"_"+str(datetime.date.today())+".zip","w") as f:
                f.write("walletProfiles.txt")
                
                os.chdir(path+ r"\Komodo\MCL")
                f.write("wallet.dat")
                
                f.close()
                
            os.chdir(path+r"\Komodo\MCL\Application Data")
            with open("walletProfiles.txt","w") as f:
                f.write("{}")
            self.copy_and_change_wallet()
            self.update_profilescombobox()
        except:
            pass
    def copy_and_change_wallet(self):
        try:
            path = os.getenv(SYSTEM_ENVIRONMENT_WORKPLACE) + r"\Komodo\MCL\wallet.dat"
            shutil.copyfile(self.dialog_window.lineEdit_4.text(),path)
            Thread(target=self.__connectForReceiveWalletInfo).start()
            receiveWalletInfos = ThreadofLoadWallet(self.dialog_window.lineEdit_3.text())
            receiveWalletInfos.ssignal.connect(self.saveWalletProfiles)
            receiveWalletInfos.start()
            
            self.dialog.close()
            
            self.newdialog = QtWidgets.QDialog()
            self.newdialog.resize(300,300)
            self.newdialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            newlabel = QtWidgets.QLabel(self.newdialog)
            newlabel.setText(self.LANG["connect_chain"])
            newlabel.setAlignment(QtCore.Qt.AlignCenter)
            newlabel.setStyleSheet("font-size:15pt;")
            newlabel.setGeometry(QtCore.QRect(50,50,200,200))
            self.newdialog.exec_()
            
        except:
            pass
    def saveWalletProfiles(self,output):
        
        time.sleep(1)
        output = json.loads(output.replace("\\r\\n","")[2:-1])
        output = {str(self.dialog_window.lineEdit.text()):dict(output)}
        with open("walletProfiles.txt","w") as f:
            json.dump(output,f)
        self.update_profilescombobox()
        self.newdialog.close()
        os.remove("closedLoops.json")
        os.remove("openLoops.json")
        
    def __connectForReceiveWalletInfo(self):
        pubkey = self.dialog_window.lineEdit_3.text()
        print("PUBKEY:",pubkey,"\n\n")
        time.sleep(1)
        x = subprocess.run("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 -pubkey="+pubkey, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        print(x)
        
        
    def loadbackup(self):

        x = loadBackup(self.LANG)
        x.done.connect(self.update_profilescombobox)
        x.show()
        
        

            
    
    def on_close(self):
        
        time.sleep(3)
        
        subprocess.run("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 -pubkey="+self.pubkey, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        time.sleep(7)
        Thread(target=self.check_connection).start()
        
        

    #if user click login, we exit login part and start main program.
    #pubkey and walletaddress will be needed by main program 
    def open_wallet_completely(self):
        global x
        jjson = ""
        with open("walletProfiles.txt","r") as f:
            jjson = json.load(f)
        try:
            self.pubkey = jjson[self.ui.comboBox.currentText()]["pubkey"]
        except:
            self.pubkey = jjson[self.ui.comboBox.currentText()]["issuer"]
            
        try:
            self.walletaddress = jjson[self.ui.comboBox.currentText()]["address"]
        except:
            self.walletaddress = jjson[self.ui.comboBox.currentText()]["myNormalAddress"]

        
        Thread(target=self.on_close).start()
        QtWidgets.QApplication.instance().quit
        self.MainWindow.close()
        
        time.sleep(1)
        
        x = sidebaar.Window()
        x.setLang(self.LANG)
        x.setpubkey(self.pubkey)
        x.setWalletAddress(self.walletaddress)
        x.initUI()
        x.show()

    def check_connection(self):
        x = subprocess.run("komodo-cli -ac_name=MCL getblockcount", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        
        if("error" in str(x.stdout)):
            subprocess.run("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 -pubkey="+self.pubkey,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

class loadBackup(QMainWindow):
    done = QtCore.pyqtSignal()
    def __init__(self,lang):
        super().__init__()
        self.setFixedSize(300,300)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 500, 500))
        
        label = QtWidgets.QLabel(self.centralwidget)
        label.setText(lang["choose_backup"])
        label.setStyleSheet("font: 10pt \\\"Comic Sans MS\\\";")
        label.setGeometry(0, 50, 300, 50)
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        
        label_2 = QtWidgets.QLabel(self.centralwidget)
        label_2.setText("")
        label_2.setStyleSheet("font: 10pt \\\"Comic Sans MS\\\";")
        label_2.setGeometry(10,150,300,50)
        label_2.setAlignment(QtCore.Qt.AlignCenter)
        
        
        
        path = "./backups/"
        files = os.listdir(path)
        filesdict = dict()
        for i in range(len(files)):
            filesdict[files[i][0:-15]]=files[i][-14:-4]
            files[i] = files[i][0:-15]
        combobox = QtWidgets.QComboBox(self.centralwidget)
        combobox.addItems(files)
        combobox.setGeometry(80, 100, 150, 40)
        combobox.currentIndexChanged.connect(lambda x:label_2.setText(lang["backup_date"]+filesdict[combobox.currentText()]))
        
        
        button = QtWidgets.QPushButton(self.centralwidget)
        button.setText(lang["load"])
        button.setStyleSheet("background-color:  #6c7585; color:#ebdeb1;font: 10pt \\\"Comic Sans MS\\\";")
        button.setGeometry(100,200,100,50)
        button.clicked.connect(lambda x:self._loadbackup(str(combobox.currentText())+"_"+filesdict[combobox.currentText()]+".zip"))
        
    def _loadbackup(self,backupname):
        appdatapath = os.getenv(SYSTEM_ENVIRONMENT_WORKPLACE) + r"\Komodo\MCL"
        with zipfile.ZipFile(r"./backups/"+backupname,"r") as f:
            f.extract("walletProfiles.txt")
            f.extract("wallet.dat",path=appdatapath)
        self.close()
        self.done.emit()
            
            
    def close(self):
        self.destroy()
        
        

_login()
