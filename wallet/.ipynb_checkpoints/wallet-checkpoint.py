import subprocess 
import os
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account
from constant import *
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
import json

def connect_wallet(keys):
    mne=os.getenv("mnemonic")

    command = 'php ..\derive -g --mnemonic=mne --cols=path,address,privkey,pubkey --format=json --numedrive=2 --coin= ETH'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()      
    keys = json.loads(output)
    return keys


connect_wallet(ETH)


def priv_key_to_account(coin,privkey):
    if coin == ETH:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        priv_eth = Account.privateKeyToAccount(privkey)

        return priv_eth
    
    elif coin == BTCTEST:
        priv_btc= PrivateKeyTestnet(priv_key)
        
        return priv_btc
    
    

    
def create_raw_tx(account, to, amount, coin):
    if coin == ETH:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": to, "value": amount}
        )
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }

    elif coin == BTCTEST:
        btc_disp = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTCTEST)])
        
        return btc_disp
    
    
    
def send_tx(account, to, amount, coin):
    if coin == ETH:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        tx = create_raw_tx(account, to, amount, coin)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        result=account.send([(to, amount, BTC)])
        return result

