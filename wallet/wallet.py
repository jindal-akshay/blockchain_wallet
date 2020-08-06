import subprocess 
import os
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account
from constant import *


def derive_wallets():
    mne=os.getenv("mnemonic")

    coin = [ETH,BTCTEST]
    
    for cointype in coin:
        if ETH:

            command = 'php ..\..\..\..\..\derive -g --mnemonic=mne --cols=path,address,privkey,pubkey --format=json --numedrive=3 --coin=ETH'

            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
        else:
            
            command = 'php ..\..\..\..\..\derive -g --mnemonic=mne --cols=path,address,privkey,pubkey --format=json --numedrive=3 --coin = BTCTEST'

            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
    return coin



def send_tx(coin, to, amount):
    if ETH:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        tx = create_raw_tx(coin, to, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()


def create_raw_tx(account, to, amount, coin):
    if ETH:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": to, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
