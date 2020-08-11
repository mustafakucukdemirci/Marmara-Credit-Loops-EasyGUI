import time
import requests
import json
import datetime

def getHistory(address):
    history_list = []
    mining_address = address
    mining_view = requests.get("http://explorer.marmara.io/insight-api-komodo/addr/"+mining_address)
    mining_json = json.loads(mining_view.text)

    money = 0.0
    total_received=0.0
    total_send = 0.0
    for i in range(len(mining_json["transactions"])):
        temp_dict = {}
        is_mined = False
        node_balance = 0.0
        #print("TRANSACTION:",i)
        txid_mining_txid = mining_json["transactions"][i]
        txid_mining_content = requests.get("http://explorer.marmara.io/insight-api-komodo/tx/"+txid_mining_txid)
        txid_content2 = json.loads(txid_mining_content.text)
        #print(json.dumps(txid_content2,indent=4))
        for win in txid_content2["vin"]:
            if("addr" not in win):
                is_mined = True
            elif(win["addr"] == mining_address):
                value = float(win["value"])
                money -= value
                total_send += value
                node_balance -= value
        
        for wout in txid_content2["vout"]:
            if("addresses" not in wout["scriptPubKey"]):
                pass
                #print("Unparsed address!!!")
            elif is_mined:
                value = float(wout["value"])
                node_balance += value
                money += value
                print("Mined:",end="")
            elif(mining_address in wout["scriptPubKey"]["addresses"]):
                value = float(wout["value"])
                money += value
                node_balance += value
                total_received += value
        #print("  Value:",value)
        current_time_tick = time.time()
        time_tick = txid_content2["time"]
        
        deltaTick = current_time_tick-time_tick
        current_date = datetime.datetime.now()
        time_of_txid = current_date - datetime.timedelta(seconds = deltaTick)
        timestr = str(time_of_txid)
        if("." in timestr):
            timestr = timestr[:-7]
        temp_dict["time"] = timestr
        temp_dict["Txid"] = mining_json["transactions"][i]
        if(is_mined):
            temp_dict["type"] = "Mined"
        elif(node_balance>0):
            temp_dict["type"] = "Received"
        elif(node_balance<0):
            temp_dict["type"] = "Send"
        elif(node_balance==0):
            temp_dict["type"] = "-"  
            
        temp_dict["Node balance"] = str(node_balance)
        history_list.append(temp_dict)

    return history_list

def run(address):
    liste = getHistory(address)

    return liste


    