import os
import sys
import json

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
