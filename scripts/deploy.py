from brownie import TapTapCoin, config, network, TapCoinGame, MockV3Aggregator
from scripts.helpful_scripts import get_account, calculate_gas_price, LOCAL_BLOCKCHAIN_ENVIORNMENTS, deploy_mocks
from web3 import Web3

users_to_transactions = {} # .2186061028000000000
gas_price = 0.15879
# Deploy TapTapCoin and TapCoinGame
accountUser1 = get_account()
accountUser2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'

def test_script_function():
    print("IT IS WORKING!!!!!")
    return "ITS WORKING!!!!!!"

def deploy_taptapcoin_and_tapcoingame():
    # account2 = get_account(1)
    print("ACCOUNT USER 1 BELOW")
    print(accountUser1)
    # print(account2)
    print(network.show_active())
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        print("NOT IN LOCAL BLOCKCHAIN ENVIRONMENTS")
        priceFeedAddress = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print("IN LOCAL BLOCKCHAIN ENVIRONMENTS")
        deploy_mocks()
        print("DEPLOYED MOCKS")
        priceFeedAddress = MockV3Aggregator[-1].address

    KEPT_BALANCE = Web3.toWei(100, "ether")
    print("BEFORE DEPLOY TTC")
    ttc = TapTapCoin.deploy({"from": accountUser1})
    print("AFTER DEPLOY TTC")
    print("BEFORE DEPLOY TCG")
    tcg = TapCoinGame.deploy(ttc.address, priceFeedAddress, {"from": accountUser1, "value": Web3.toWei(0.05, "ether")})
    print("AFTER DEPLOY TCG")
    tx = ttc.transfer(tcg.address, ttc.totalSupply() - KEPT_BALANCE, {"from": accountUser1})
    print("AFTER FIRST TRANSACTION")
    tx.wait(1)
    print("WAITED FOR FIRST TRANSACTION")
    print("DEPLOYED TAPTAP COIN")
    print("ADDRESS BELOW")
    print(tcg.address)
    print("ABI BELOW")
    print(tcg.abi)
    print("BTYECODE BELOW")
    print(tcg.bytecode)
    print(tcg.getTotalTapTapCoinSupply({"from": accountUser1}))
    print(tx.gas_price)
    # account2 = accounts[1]
    return ttc, tcg


# Add User wallet
def addUserWallet(tcg, newAccount, account):
    # call function to add wallet with parameters
    tx = tcg.addWallet(newAccount, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    tx.wait(1)
    # newGasPrice = str(tx.gas_price)[:1] + "." + str(tx.gas_price)[1:]
    # print(float(newGasPrice))
    addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
    users_to_transactions[newAccount] = addingTransaction
    print("ADDED WALLET SUCCESSFULLY")
    print(tx.gas_price)
    print(tcg.getTotalTransactions(newAccount))
    # get transaction and look at amount gas cost - use testnet

# Pass RECAPTCHA
def faceIdCheck(tcg, newAccount, account):
    # pass or fail RECAPTCHA
    tx = tcg.faceIdCheck(newAccount, "TEMPORARYRECAPTCHACODE", users_to_transactions[newAccount],{"from": account})
    tx.wait(1)
    addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
    users_to_transactions[newAccount] = addingTransaction
    print("PASSED RECAPTCHA")
    print(tx.gas_price)

def updatePlayersWins(tcg, winner, loser, hasEvent, account):
    #update players wins
    tx = tcg.updatePlayersWins(winner, loser, users_to_transactions[winner], users_to_transactions[loser], True, {"from": account})
    tx.wait(1)
    if hasEvent:
        print("TRANSACTION PRICE BELOW")
        print(tx.events[0])
    else:
        print("NO EVENT YET")
    print("GAS PRICE BELOW")
    print(tx.gas_price)
    # try:
    #     # print("LESS THAN HALF BELOW")
    #     # tx.events[0]["lessThanHalf"]
    #     # print("WINNINGS EVENT BELOW")
    #     # tx.events[0]["winningsEvent"]
    # 13116366169200000000
    # 20000000000000000000
    # 50735667174023340000
    # 512119120000000
    ## ADJUST THE CALCULATIONS SOMEWHERE OR DO THEM BY HAND AT FIRST
    # except:
    #     print("NO EVENT DATA YET")
# HandleOutcome (winner/loser)
    # check to make sure both players have wallets added
    # check to make sure both players have passed RECAPTCHA
    # take away loser streak
    # update winner streak
    # check if winner passed specific streak limit then award coin
    # send amount awarded back in terms of USD
    # get transaction and look at amount gas cost - use testnet
    # https://sepolia.infura.io/v3/6ee647761d0549c6a44f728ef28d28a5
    


def main():
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^ BEGINNING ^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # test_script_function()
    ttc, tcg = deploy_taptapcoin_and_tapcoingame() # STEP 1
    print("*********************************************************")
    print("*********************************************************")
    print("##### TAPTAPCOIN AND TAPCOINGAME HAVE BEEN DEPLOYED #####")
    print("*********************************************************")
    print("*********************************************************")
    # addUserWallet(tcg, accountUser1, accountUser1)  # STEP 2
    # print("*********************************************************")
    # print("*********************************************************")
    # print("################ ACCOUNT 1 WALLET ADDED #################")
    # print("*********************************************************")
    # print("*********************************************************")
    # addUserWallet(tcg, accountUser2, accountUser1) # STEP 3
    # print("*********************************************************")
    # print("*********************************************************")
    # print("################ ACCOUNT 2 WALLET ADDED #################")
    # print("*********************************************************")
    # print("*********************************************************")
    # faceIdCheck(tcg, accountUser1, accountUser1) # STEP 4
    # print("*********************************************************")
    # print("*********************************************************")
    # print("############## ACCOUNT 1 PASSED RECAPTCHA ###############")
    # print("*********************************************************")
    # print("*********************************************************")
    # faceIdCheck(tcg, accountUser2, accountUser1) # STEP 5
    # print("*********************************************************")
    # print("*********************************************************")
    # print("############## ACCOUNT 2 PASSED RECAPTCHA ###############")
    # print("*********************************************************")
    # print("*********************************************************")
    # updatePlayersWins(tcg, accountUser1, accountUser2, False, accountUser1) # STEP 6
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$ UPDATED PLAYER WINS 1 $$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # updatePlayersWins(tcg, accountUser1, accountUser2, False, accountUser1) # STEP 7
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$ UPDATED PLAYER WINS 2 $$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # updatePlayersWins(tcg, accountUser1, accountUser2, False, accountUser1)  # STEP 8
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$ UPDATED PLAYER WINS 3 $$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # updatePlayersWins(tcg, accountUser1, accountUser2, False, accountUser1)  # STEP 9
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$ UPDATED PLAYER WINS 4 $$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # updatePlayersWins(tcg, accountUser1, accountUser2, False, accountUser1)  # STEP 10
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$ FINSIHED $$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print(tcg.getTotalTransactions(accountUser1, {"from": accountUser1}))
    # print(tcg.getPrice({"from": accountUser1}))
    # print(tcg.getCurrentActualUsdCost({"from": accountUser1}))
    # print(tcg.testCalculateWinnings(accountUser1, {"from": accountUser1}))
    # print(tcg.getConversion(accountUser1, {"from": accountUser1}))
    # print(tcg.getUsersStreakCount(accountUser1))
    # weiAmount = Wei("1 ether")
    # transaction_sum = 2186061028200000000
    # test = transaction_sum / weiAmount
    # print("Wei amount below")
    # print(test)
    # 1841085635180000000000
    # 0.000543157787390064 0000000
    # 2.186088486960749999