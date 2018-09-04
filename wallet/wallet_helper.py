import requests
import json
import base64
import time
import sys
import random

url = "http://localhost:8383"
rpcuser = "ckrpc"
rpcpassword = "jxjQ9TgRqIyIlatz7a1TNjEJ2TNQ46M8K9WFEM9VXFQ="
#walletpassword = "distance"
#walletaccount = "nifty"
fee = 20000
#publicKey = "BLD6fw7+X/a2BBwYBEUOpwjNaSmpnnv9Jpj59iv4f7TIAQLOFR40Zg4Kh0fnoXRXqhYQGePJDSnWgaMl8uV8uCQ="

def request(method, params):
    unencoded_str = rpcuser + ":" + rpcpassword
    encoded_str = base64.b64encode(unencoded_str.encode())
    headers = {
        "content-type": "application/json",
        "Authorization": "Basic " + encoded_str.decode('utf-8')}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response

def get_compiled_code():
    with open("/home/luke/Documents/xcoin/contract.lua") as contract_file:
        contract_code = contract_file.read()
    
    compiled_code = request("compilecontract", {"code": contract_code})["result"]

    return compiled_code

def get_xcoins(compiled_code, user):
    utxos = request("listunspentoutputs", {"password": user.profile.wallet_password, "account": user.profile.wallet_account})["result"]["outputs"]
    xcoins = []
    for utxo in utxos:
        print(utxo)
        if utxo["data"]["contract"] == compiled_code:
            xcoins.append(utxo)
    
    return xcoins

def send_xcoins(compiled_code, address, amount, user):
    xcoins = get_xcoins(compiled_code, user)
    total = 0
    toSpends = []
    for coin in xcoins:
        if total < amount:
            total += coin["data"]["value"]
            toSpends.append(coin)
        else:
            break
    
    if total >= amount:
        inputs = []
        for toSpend in toSpends:
            input = {"outputId": toSpend["id"]} # does this work?
            inputs.append(input)
    
        toThem = {
            "value": 50000,
            "nonce": random.randint(1, 64000),
            "data": {"publicKey": address, "value": amount, "contract": compiled_code},
        }
        change = {
            "value": 50000,
            "nonce": random.randint(1, 64000),
            "data": {"publicKey": user.profile.public_key, "value": total - amount, "contract": compiled_code}
        }

        transaction = {
            "inputs": [inputs], 
            "outputs": [toThem, change], 
            "timestamp": int(time.time()),
        }

        print(json.dumps(transaction, sort_keys=True, indent=4))

        signed = request("signtransaction", {"transaction": transaction, "password": user.profile.wallet_password})["result"]

        # broadcast the transaction on the network
        success = request("sendrawtransaction", {"transaction": signed})["result"]
        return success
    else:
        return (False, "Not enough value")


def tally_value(compiled_code, user):
    xcoins = get_xcoins(compiled_code, user)
    total = 0
    for xcoin in xcoins:
        total += xcoin["data"]["value"]
    
    return total