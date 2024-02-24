from brownie import accounts, network, config, Wei, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
FORKED_LOCAL_ENVIORNMENTS = ["mainnet-fok", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIORNMENTS = ["development", "ganache_local"]

def get_account(index=0, id=None, user2=False):
    if index:
        print("ACCOUNTS BELOW *******************")
        print(accounts)
        return accounts[index]
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS 
    or network.show_active() in FORKED_LOCAL_ENVIORNMENTS):
        return accounts[0]
    if user2:
        return accounts.add(config["wallets"]["from_key2"])
    else:
        return accounts.add(config["wallets"]["from_key"])

# GET THE FUNDS
def calculate_gas_price(gasPrice, gasLimit):
    print("GAS PRICE BELOW:")
    print(gasPrice)
    print("GAS LIMIT BELOW")
    print(gasLimit)
    sum = gasPrice * gasLimit
    print(sum)
    finalSum = Wei(f"{sum} gwei")
    print(finalSum)
    return finalSum

def deploy_mocks():
    print("IN DEPLOY MOCKS")
    if len(MockV3Aggregator) <= 0:
        print("IT IS DEPLOYING A NEW MOCK")
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    else:
        print("NO NEW MOCK DEPLOYED")