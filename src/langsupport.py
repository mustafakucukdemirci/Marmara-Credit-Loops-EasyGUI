import os
import sys
import json
from PyQt5 import  QtGui, QtWidgets
from github import Github
from bs4 import BeautifulSoup
import requests

class language():
    LANG = ""
    def __init__(self,lang,path):
        os.chdir(path)
        if("lang" in os.listdir()):
            os.chdir("lang")
            with open(lang+".json","r",encoding="utf-8") as f:
                text = f.read()
                self.LANG = json.loads(text)
            os.chdir(os.path.dirname(os.getcwd()))
            
                
        else:
            raise Exception("Lang directory doesn't exist")
def language_list():
    os.chdir("lang")
    file_list = os.listdir()
    for i in file_list:
        if ".json" not in i:
            file_list.remove(i)
        else:
            file_list[file_list.index(i)] = file_list[file_list.index(i)][:-5]
    os.chdir(os.path.dirname(os.getcwd()))
    return file_list

def change_language_value(newLanguage,loginWindow,lang):

    with open("cfg.txt","r") as f:
        _json = json.loads(f.read())
    _json["language"] = newLanguage.currentText()
    with open("cfg.txt","w") as f:
        f.write(json.dumps(_json,indent=4))
    x = QtWidgets.QMessageBox()
    x.setText(lang["lang_change_text"])
    x.setWindowTitle("Error")
    x.setIcon(QtWidgets.QMessageBox.Information)
    x.exec_()

def downloadLanguages():
    langs = []
    x = requests.get("https://github.com/paragomia/Marmara-Credit-Loops-EasyGUI/tree/master/lang")
    soup = BeautifulSoup(x.text, 'html.parser')
    for x in soup.find_all('a'):
        if(".json" in str(x.get("href"))):
            x = str(x.get("href")).split("/")
            langs.append(x[-1])
    if("lang" not in os.listdir()):
        os.mkdir("lang")
    os.chdir("lang")
    dledLanguages = os.listdir()
    for i in langs:
        if i not in dledLanguages:
            with open(i,"w",encoding="utf-8") as f:
                f.write(requests.get("https://combinatronics.com/paragomia/Marmara-Credit-Loops-EasyGUI/master/lang/"+i).text)
    os.chdir(os.path.dirname(os.getcwd())) 
    
    
    
    