import os
import sys
import json
from PyQt5 import  QtGui, QtWidgets
from github import Github

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
#    os.chdir("lang")
    
    g = Github("0d49e540e3ddc52509"+"1b28e248ef007fefb09b2a")

    repo = g.get_repo("paragomia/Marmara-Credit-Loops-EasyGUI")
    
    currentFiles = os.listdir()
    for file in repo.get_contents("lang"):
        if file.name not in currentFiles and file.name != "readme.md":
            with open(file.name,"w") as f:
                f.write(file.content)
    os.chdir(os.path.dirname(os.getcwd()))
    
downloadLanguages()