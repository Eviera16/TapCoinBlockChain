from brownie import accounts, TapTapCoin, TapCoinGame, exceptions, network, config
import pytest
from web3 import Web3
from scripts.helpful_scripts import get_account, calculate_gas_price, LOCAL_BLOCKCHAIN_ENVIORNMENTS
import time


users_to_transactions = {}
gas_price = 1.5

def test_add_user_wallet():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        pytest.skip()
    # Arrange
    price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    account = get_account()
    ttc = TapTapCoin.deploy({"from": account})
    tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
    # Act
    tcg.addWallet(account,"TEMPORARYADDWALLETPASSCODE", {"from": account})
    # Assert
    assert tcg.checkForUser(account, {"from": account}) == True

# def test_face_id_check():
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
    #     pytest.skip()
    # # Arrange
    # price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    # account = get_account()
    # ttc = TapTapCoin.deploy({"from": account})
    # tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
    # tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE", {"from": account})
    # # Act
    # tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account})
    # # Assert
    # assert tcg.checkUserFaceIdChecked(account) == True

# Figure this out at the end of the list !!!!!!
# def test_fail_face_id_check():
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     # Arrange
#     price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
#     account = get_account()
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
#     # Act
#     account3 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
#     tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE", {"from": account})
#     # Assert
#     with pytest.raises(exceptions.VirtualMachineError):
#         tcg.faceIdCheck(account, "INCORRECTCODEHERE",2186061028200000000, {"from": account, "gas_limit":12000000,"allow_revert":True})
#     with pytest.raises(exceptions.VirtualMachineError):
#         tcg.faceIdCheck(account3, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account, "gas_limit":12000000,"allow_revert":True})

# def test_users_streaks_adding_correctly():
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
    #     pytest.skip()
    # #Arrange
    # price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    # account = get_account()
    # account2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
    # print("ACCOUNT 2 BELOW")
    # print(account2)
    # ttc = TapTapCoin.deploy({"from": account})
    # tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
    # #Act
    # # Add both users wallets
    # tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # # Users Enter first game
    # tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
    # tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
    # # Users finish first game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter second game
    # # Users finish second game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter third game
    # # Users finish third game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter fourth game
    # # Users finish fourth game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter fifth game
    # # Users finish fifth game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # #Assert
    # assert tcg.getUsersStreakCount(account2) == 0
    # assert tcg.getUsersStreakCount(account) == 5

# def test_winnings_calculated_correctly():
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
    #     pytest.skip()
    # #Arrange
    # price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    # account = get_account()
    # account2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
    # print("ACCOUNT 2 BELOW")
    # print(account2)
    # ttc = TapTapCoin.deploy({"from": account})
    # tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
    # tx = ttc.transfer(tcg.address, ttc.totalSupply(), {"from": account})
    # tx.wait(1)
    # tx1 = tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # tx1.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx1.gas_limit)
    # users_to_transactions[account] = addingTransaction
    # tx2 = tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # tx2.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx2.gas_limit)
    # users_to_transactions[account2] = addingTransaction
    # tx3 = tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", users_to_transactions[account],{"from": account})
    # tx3.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx3.gas_limit)
    # users_to_transactions[account] = addingTransaction
    # tx4 = tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", users_to_transactions[account2],{"from": account})
    # tx4.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx4.gas_limit)
    # users_to_transactions[account2] = addingTransaction
    # #Act
    # tx5 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
    # tx5.wait(1)
    # tx6 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
    # tx6.wait(1)
    # tx7 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
    # tx7.wait(1)
    # tx8 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
    # tx8.wait(1)
    # tx9 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], True, 73, {"from": account})
    # tx9.wait(1)
    # assert tcg.getTransactionData(account, 7, {"from": account}) < 20000000000000000000
    # assert 20000000000000000000 - tcg.getTransactionData(account, 7, {"from": account}) > 20000000000000000000/2

# TEST AGAIN
# def test_winner_receives_correct_winnings():
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
    #     pytest.skip()
    # #Arrange
    # price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    # account = get_account()
    # account2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
    # print("ACCOUNT 2 BELOW")
    # print(account2)
    # ttc = TapTapCoin.deploy({"from": account})
    # tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
    # originalWinnerWalletAmount = account.balance()
    # # tx = ttc.transfer(tcg.address, ttc.totalSupply(), {"from": account})
    # # tx.wait(1)
    # tx1 = tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # tx1.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx1.gas_limit)
    # users_to_transactions[account] = addingTransaction
    # tx2 = tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # tx2.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx2.gas_limit)
    # users_to_transactions[account2] = addingTransaction
    # tx3 = tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", users_to_transactions[account],{"from": account})
    # tx3.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx3.gas_limit)
    # users_to_transactions[account] = addingTransaction
    # tx4 = tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", users_to_transactions[account2],{"from": account})
    # tx4.wait(1)
    # addingTransaction = calculate_gas_price(gas_price, tx4.gas_limit)
    # users_to_transactions[account2] = addingTransaction
    # #Act
    # tx5 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx5.wait(1)
    # tx6 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx6.wait(1)
    # tx7 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx7.wait(1)
    # tx8 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx8.wait(1)
    # tx9 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], True, 73, {"from": account})
    # tx9.wait(1)
    # winningsAmount = tcg.calculateWinnings(account, 73, {"from": account})
    # print("WINNINGS AMOUNT")
    # print(winningsAmount)
    # print("ORIGINAL WINNER WALLET AMOUNT")
    # print(originalWinnerWalletAmount)
    # print("ACCOUNT BALANCE")
    # print(account.balance())
    # print("RETURN VALUE")
    # print(tx9.return_value)
    # # Call the below function through an if statment based on the return value from tx9
    # tx10 = tcg.awardTapTapCoin(account, {"from": account, "value": tx9.return_value})
    # tx10.wait(1)
    # #Assert
    # assert account.balance() == originalWinnerWalletAmount + winningsAmount


# def test_setting_transaction_prices_correctly():
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     #Arrange
#     price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
#     account = get_account()
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
#     account2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
#     tx = ttc.transfer(tcg.address, ttc.totalSupply(), {"from": account})
#     tx.wait(1)
#     tx1 = tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     tx1.wait(1)
    # addingTransaction_user1_1 = calculate_gas_price(gas_price, tx1.gas_limit)
    # users_to_transactions[account] = addingTransaction_user1_1
    # tx2 = tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # tx2.wait(1)
    # addingTransaction_user2_1 = calculate_gas_price(gas_price, tx2.gas_limit)
    # users_to_transactions[account2] = addingTransaction_user2_1
    # tx3 = tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", users_to_transactions[account],{"from": account})
    # tx3.wait(1)
    # addingTransaction_user1_2 = calculate_gas_price(gas_price, tx3.gas_limit)
    # users_to_transactions[account] = addingTransaction_user1_2
    # tx4 = tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", users_to_transactions[account2],{"from": account})
    # tx4.wait(1)
    # addingTransaction_user2_2 = calculate_gas_price(gas_price, tx4.gas_limit)
    # users_to_transactions[account2] = addingTransaction_user2_2
    #Act
    # tx5 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx5.wait(1)
    # addingTransaction_users_3 = calculate_gas_price(gas_price, tx5.gas_limit)
    # users_to_transactions[account] = addingTransaction_users_3
    # users_to_transactions[account2] = addingTransaction_users_3
    # tx6 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx6.wait(1)
    # addingTransaction_users_4 = calculate_gas_price(gas_price, tx6.gas_limit)
    # users_to_transactions[account] = addingTransaction_users_4
    # users_to_transactions[account2] = addingTransaction_users_4
    # tx7 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx7.wait(1)
    # addingTransaction_users_5 = calculate_gas_price(gas_price, tx7.gas_limit)
    # users_to_transactions[account] = addingTransaction_users_5
    # users_to_transactions[account2] = addingTransaction_users_5
    # tx8 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
    # tx8.wait(1)
    # addingTransaction_users_6 = calculate_gas_price(gas_price, tx8.gas_limit)
    # users_to_transactions[account] = addingTransaction_users_6
    # users_to_transactions[account2] = addingTransaction_users_6
    # tx9 = tcg.updatePlayersWins(account, account2, users_to_transactions[account2], users_to_transactions[account], True, 73, {"from": account})
    # tx9.wait(1)
    #Assert
    # assert tcg.getTransactionData(account, 0, {"from": account}) == tcg.getCurrentActualUsdOneCentCost({"from": account})
    # assert tcg.getTransactionData(account, 1, {"from": account}) == addingTransaction_user1_1
    # assert tcg.getTransactionData(account, 1, {"from": account}) == addingTransaction_user1_1
    # assert tcg.getTransactionData(account, 3, {"from": account}) == addingTransaction_users_3
    # assert tcg.getTransactionData(account, 4, {"from": account}) == addingTransaction_users_4
    # assert tcg.getTransactionData(account, 5, {"from": account}) == addingTransaction_users_5
    # assert tcg.getTransactionData(account, 6, {"from": account}) == addingTransaction_users_6

# def test_users_games_adding_correctly():
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
    #     pytest.skip()
    # #Arrange
    # price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    # account = get_account()
    # account2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
    # print("ACCOUNT 2 BELOW")
    # print(account2)
    # ttc = TapTapCoin.deploy({"from": account})
    # tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
    # #Act
    # # Add both users wallets
    # tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
    # # Users Enter first game
    # tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
    # tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
    # # Users finish first game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter second game
    # # Users finish second game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter third game
    # # Users finish third game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter fourth game
    # # Users finish fourth game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # # Users Enter fifth game
    # # Users finish fifth game
    # tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
    # #Assert
    # assert tcg.getUsersGamesCount(account2, {"from": account}) == 5
    # assert tcg.getUsersGamesCount(account, {"from": account}) == 5

# def test_check_wait_time_ends_correctly():
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     # Arrange
#     price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
#     account = get_account()
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
#     tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE", {"from": account})
#     # Act
#     tcg.setUsersGamesTo100(account, {"from": account})
#     account2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
#     tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE", {"from": account})
#     tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account})
#     tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account})
#     # Assert
#     assert tcg.checkUserFaceIdChecked(account) == True
