import tkinter
from PyQt5.QtWidgets import *
from tkinter import ttk,filedialog
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



class ThreadofLoadWallet(QtCore.QThread):
    ssignal = QtCore.pyqtSignal(object)
    def __init__(self,pubkey):
        self.pubkey=pubkey
        QtCore.QThread.__init__(self)
    def run(self):
        while True:
            try:
                x = subprocess.run("komodo-cli -ac_name=MCL marmarainfo 0 0 0 0 "+self.pubkey, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                if(str(x.stdout) != "b''"):
                    output = str(x.stdout)
                    subprocess.run("komodo-cli -ac_name=MCL stop")
                    self.ssignal.emit(output)
                    break
            except:
                print(x)
                continue
            
            
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
        print(self.wallet_adress,self.pubkey,self.priv_key)
        self.loopssignal.emit([self.wallet_adress,self.pubkey,self.priv_key])

    def run(self):
        self.process()

    def process(self):
        count = 2
        while True:
            if(count < 0 and count%2 == 0):
                self.startchainagainsignal.emit([ ])
            self.wallet_adress = subprocess.run("komodo-cli.exe -ac_name=MCL getnewaddress", stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)  
            self.wallet_adress = str(self.wallet_adress.stdout)[2:-5]
            print("wallet address",self.wallet_adress)
            self.pubkey = subprocess.run("komodo-cli.exe -ac_name=MCL validateaddress "+self.wallet_adress, stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE)  #cüzdan oluşturuoruz
            self.pubkey = str(self.pubkey.stdout)[2:-5]#başında sonunda çıkan gereksiz "'" gibi şeylerden kurtuluyoruz
            self.pubkey = self.pubkey.replace("\\r\\n","")#json a karışıklık çıkartan bunlardan kurtuluyoruz
            print("pubkey = ",self.pubkey)
            time.sleep(1)
            self.priv_key = subprocess.run("komodo-cli.exe -ac_name=MCL dumpprivkey "+self.wallet_adress, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            self.priv_key = str(self.priv_key.stdout)[2:-5]
            print(self.priv_key)
            if(self.wallet_adress == "" or self.pubkey == "" or self.priv_key == "" or "error" in self.wallet_adress or "error" in self.pubkey or "error" in self.priv_key):
                count -=1
                continue
            else:
                self.emitter()
                break

class newAccount(QMainWindow):
    
    def __init__(self, parent=None):
        super(newAccount, self).__init__(parent)
        self.setFixedSize(600,450)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 600, 450))
        
        self.gridlayout = QtWidgets.QGridLayout(self.centralwidget)
        
        self.setCentralWidget(self.centralwidget)
        self.button = QtWidgets.QPushButton()
    def controller(self):
        
        self.profileName = self.enterprofilenameLE.text()
        
        self.clearScreen()
        waitingLabel = QtWidgets.QLabel("Zincire bağlanılıyor...")
        waitingLabel.setAlignment(QtCore.Qt.AlignCenter)
        waitingLabel.setStyleSheet("font-size:30pt")
        self.gridlayout.addWidget(waitingLabel,0,0)
        self.gridlayout.update()
        
        self.threader = ControlThread()
        self.threader.loopssignal.connect(self.save_new_wallet)
        self.threader.startchainagainsignal.connect(lambda:Thread(target=self.start_chain_without_pubkey).start())
        self.threader.start()
        
        
    def _create_new_account(self):
        self.clearScreen()
        Thread(target=self.start_chain_without_pubkey).start()
        
        
        enterprofilenamelabel = QtWidgets.QLabel("Profil adı giriniz:")
        self.gridlayout.addWidget(enterprofilenamelabel,0,0,1,2)
        
        
        self.enterprofilenameLE = QtWidgets.QLineEdit()
        self.gridlayout.addWidget(self.enterprofilenameLE,0,2,1,3)
        
        
        
        self.button.setText("Oluştur")
        self.button.clicked.connect(self.controller)
        
        self.gridlayout.addWidget(self.button,3,2,1,1)
        
        self.show()
        
        
    def save_new_wallet(self,liste):

        wallet_address = liste[0]
        pubkey = liste[1]
        priv_key = liste[2]
        

        x = QtWidgets.QFileDialog.getExistingDirectory()
        print("X:",x,"  profile_name:",self.profileName)
        with open(x+r"/"+self.profileName+".txt","w") as f:
            pubkey = pubkey.replace("'",'"')
            pubkey = pubkey.replace(" ","")
            dictionary_pubkey = dict(json.loads(pubkey))
            dictionary = {priv_key:dict(dictionary_pubkey)}
            f.write(json.dumps(dictionary,indent=4))
        print("whaat\n\n\n\n\n\n\n\n")
        self.add_profile(self.profileName,pubkey)
        subprocess.Popen("komodo-cli.exe -ac_name=MCL stop")
        self.destroy()
        self.update_profilescombobox()
        
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
        self.chain = subprocess.run("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 ", stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        print("this is chain",self.chain)
        
class _login():
    def stopper(self):
        subprocess.run("komodo-cli.exe -ac_name=MCL stop", stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True, stdin=subprocess.PIPE)

    def __init__(self):
        Thread(target=self.stopper).start()
        path = os.getenv('APPDATA')
        try:
            os.chdir(path+r"\Komodo\MCL\Application Data")
        except:
            os.mkdir(path+r"\Komodo\MCL\Application Data")
            os.chdir(path+r"\Komodo\MCL\Application Data")
        #very starting screen, if files are full in zcash, this screen pass very fast.
        if "walletProfiles.txt" not in os.listdir():
            with open("walletProfiles.txt","w") as f:
                f.write("{}")
        
        self.downloading_screen = tkinter.Tk()
        self.downloading_screen.attributes("-topmost", True)
        self.downloading_screen.overrideredirect(True)
        self.downloading_screen.geometry("200x200+900+400")
        
        self.giris()
        self.downloading_screen.mainloop()
        
        self.actualy_login()
        
    def giris(self):
        self.label2 = tkinter.Label(self.downloading_screen,text="\n\n\n\n\n")
        self.label2.grid(row=0,column=0)
        self.label3 = tkinter.Label(self.downloading_screen,text="            ")
        self.label3.grid(row=1,column=0)
        self.label = tkinter.Label(self.downloading_screen,text="Checking files...")
        self.label.grid(row=1,column=1)
        self.label.update()
        #Check if file is missing
        path = os.getenv('APPDATA') + "\ZcashParams"
        files = os.listdir(path)
        check_list = ["sapling-output.params","sapling-spend.params","sprout-groth16.params","sprout-proving.key","sprout-verifying.key"]
        download = False
        for i in check_list:
            self.label.configure(text="checking "+str(i))
            self.label.update()
            if i not in files:
                download = True
        
        #if any of file is missing, download will be true so we run fetch-params
        if(download):
            self.label.configure(text="We are downloading\n   missing files...")
            self.label.update()
            x = (subprocess.run("fetch-params.bat", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,stdin=subprocess.PIPE))
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
        #login ana sayfası
        
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
        
        
        
        self.ui.pushButton.clicked.connect(self.open_wallet_completely)
        self.ui.pushButton_2.clicked.connect(self.importwallet)
        self.ui.pushButton_3.clicked.connect(self.loadbackup)
        
        self.ui.pushButton_4.clicked.connect(self.new_account._create_new_account)
        
        self.MainWindow.show()
        sys.exit(self.app.exec_())
        
        
        
        
    def update_profilescombobox(self):
        #yeni pubkey alma, cüzdan import etme vb. işlemlerde bu fonk. ile profil listesini güncellicez
        self.ui.comboBox.clear()
  
        self.ui.comboBox.addItems(self.read_profiles())
        

        


    def read_profiles(self):
        with open("walletProfiles.txt","r") as f:
            text = f.read()
            _json = dict(json.loads(text))
        profile_list = list()
        for i in _json.keys():
            profile_list.append(i)
        return profile_list
        
    
    def importwallet(self):
        self.importWallet = QtWidgets.QMainWindow()
        self.importWallet.setFixedSize(600,450)
        
        centralWidget = QtWidgets.QWidget(self.importWallet)
        
        layout = QtWidgets.QGridLayout(centralWidget)
        
        self.importWallet.setCentralWidget(centralWidget)
        
        layout.addWidget(QtWidgets.QLabel("Eski cüzdanınızı yedekleyeceğiz. Yedek dosyasına bir isim veriniz:"),0,0,1,3)
        
        self.idLE = QtWidgets.QLineEdit()
        
        layout.addWidget(self.idLE,0,3,1,5)
        
        layout.addWidget(QtWidgets.QLabel("Cüzdan Yolu:"),1,0,1,1)
        
        self.pathLE = QtWidgets.QLineEdit()
        layout.addWidget(self.pathLE,1,3,1,4)
        
        pathButton = QtWidgets.QPushButton()
        pathButton.setText("Cüzdan seç")
        pathButton.clicked.connect(lambda:self.pathLE.setText(str(QtWidgets.QFileDialog.getOpenFileName())[2:-19]))
        
        layout.addWidget(pathButton,1,8,1,1)
        
        layout.addWidget(QtWidgets.QLabel("Cüzdan'ın Pubkeyini Giriniz:"),2,0,1,2)
        
        self.pubkeyLE = QtWidgets.QLineEdit()
        layout.addWidget(self.pubkeyLE,2,2,1,6)
        
        button = QtWidgets.QPushButton()
        button.setText("Yükle")
        button.clicked.connect(lambda:self.backup_import())
        layout.addWidget(button,4,3,1,1)
        
        
        self.importWallet.show()
        

    def backup_import(self):
        
        name = self.idLE.text()
        path = os.getenv('APPDATA')
        
        os.chdir(path+r"\Komodo\MCL\Application Data")
        try:
            os.mkdir("backups")
        except:
            pass
        
        with zipfile.ZipFile(".\\backups\\"+name+":"+str(datetime.date.today())+".zip","w") as f:
            f.write("walletProfiles.txt")
            
            os.chdir(path+ r"\Komodo\MCL")
            f.write("wallet.dat")
            
            f.close()
            
        os.chdir(path+r"\Komodo\MCL\Application Data")
        with open("walletProfiles.txt","w") as f:
            f.write("{}")
        self.copy_and_change_wallet()
        self.update_profilescombobox()
    def copy_and_change_wallet(self):
        path = os.getenv('APPDATA') + r"\Komodo\MCL\wallet.dat"
        shutil.copyfile(self.pathLE.text(),path)
        Thread(target=self.__connectForReceiveWalletInfo).start()
        print("connectforreceivewallet started")
        receiveWalletInfos = ThreadofLoadWallet(self.pubkeyLE.text())
        receiveWalletInfos.ssignal.connect(self.saveWalletProfiles)
        receiveWalletInfos.start()
        self.importWallet.destroy()
        
        self.x = connecting_chain()
        self.x.show()
        
        print("Second Thread Started")
        
    def saveWalletProfiles(self,output):
        
        time.sleep(1)
        print(output)
        output = json.loads(output.replace("\\r\\n","")[2:-1])
        output = {"Varsayılan":dict(output)}
        print(output)
        with open("walletProfiles.txt","w") as f:
            json.dump(output,f)
        self.x.close()
        self.update_profilescombobox()
        
    def __connectForReceiveWalletInfo(self):
        pubkey = self.pubkeyLE.text()
        subprocess.run("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 -pubkey="+pubkey)
        
        
        
    def loadbackup(self):

        x = loadBackup()
        x.show()
        
        

            
    
    def on_close(self):
        
        print("Zincir kapanıyor...\n")
        time.sleep(3)
        
        openchain = subprocess.Popen("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 -pubkey="+self.pubkey)

        time.sleep(7)
        print("sürebitti")
        Thread(target=self.check_connection).start()
        
        

        
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
        self.MainWindow.close()
        
        time.sleep(1)
        
        x = sidebaar.Window()
        x.setpubkey(self.pubkey)
        x.setWalletAddress(self.walletaddress)
        x.initUI()
        x.show()

    def check_connection(self):
        x = subprocess.run("komodo-cli -ac_name=MCL getblockcount", stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True, stdin=subprocess.PIPE)
        
        if("error" in str(x.stdout)):
            subprocess.Popen("komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 -pubkey="+self.pubkey)

class connecting_chain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(300,300)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 200, 200))
        
        label = QtWidgets.QLabel(self.centralwidget)
        label.setText("Zincire Bağlanılıyor...")
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        label.setGeometry(0, 50, 200, 150)
        
    def close(self):
        self.destroy()
        
class loadBackup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300,300)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 500, 500))
        
        label = QtWidgets.QLabel(self.centralwidget)
        label.setText("Backup dosyanızı seçiniz:")
        label.setGeometry(8, 10, 100, 100)
        
        path = "./backups/"
        files = os.listdir(path)
        combobox = QtWidgets.QComboBox(self.centralwidget)
        combobox.addItems(files)
        combobox.setGeometry(115, 40, 150, 40)
        
        button = QtWidgets.QPushButton(self.centralwidget)
        button.setText("Yükle")
        button.setGeometry(160,120,50,20)
        button.clicked.connect(lambda x:self._loadbackup(str(combobox.currentText())))
        
    def _loadbackup(self,backupname):
        appdatapath = os.getenv('APPDATA') + r"\Komodo\MCL"
        with zipfile.ZipFile(r"./backups/"+backupname,"r") as f:
            f.extract("walletProfiles.txt")
            f.extract("wallet.dat",path=appdatapath)
        self.close()
            
            
    def close(self):
        self.destroy()
        
_login()
