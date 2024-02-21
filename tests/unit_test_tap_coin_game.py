from brownie import accounts, TapTapCoin, TapCoinGame, exceptions, network, MockV3Aggregator
import pytest
from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIORNMENTS, calculate_gas_price, deploy_mocks
import time

users_to_transactions = {}
gas_price = 1.5
# faceIdCheck

# def test_add_user_wallet():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     # Arrange
#     deploy_mocks()
#     priceFeedAddress = MockV3Aggregator[-1].address
#     account = accounts[0]
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, priceFeedAddress, {"from": account})
#     # Create new account to add
#     accounts.add()
#     account2 = accounts[1]
#     # Act
#     tcg.addWallet(account2,"TEMPORARYADDWALLETPASSCODE", {"from": account})
#     # Assert
#     assert tcg.checkForUser(account2, {"from": account}) == True

# def test_pass_face_id_check():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     # Arrange
#     deploy_mocks()
#     price_feed_address = MockV3Aggregator[-1].address
#     account = accounts[0]
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
#     account2 = accounts[1]
#     tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE", {"from": account})
#     # Act
#     tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account})
#     # Assert
#     assert tcg.checkUserFaceIdChecked(account2) == True

# def test_fail_face_id_check():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     # Arrange
#     deploy_mocks()
#     price_feed_address = MockV3Aggregator[-1].address
#     account = accounts[0]
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
#     account2 = accounts[1]
#     account3 = accounts[2]
#     tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE", {"from": account})
#     # Act
#     # Assert
#     with pytest.raises(exceptions.VirtualMachineError):
#         tcg.faceIdCheck(account2, "INCORRECTCODEHERE",2186061028200000000, {"from": account})
#     with pytest.raises(exceptions.VirtualMachineError):
#         tcg.faceIdCheck(account3, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account})

# def test_users_streaks_adding_correctly():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     #Arrange
#     deploy_mocks()
#     priceFeedAddress = MockV3Aggregator[-1].address
#     account = accounts[0]
#     account2 = accounts[1]
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, priceFeedAddress, {"from": account})
#     #Act
#     # Add both users wallets
#     tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     # Users Enter first game
#     tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
#     tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
#     # Users finish first game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter second game
#     # Users finish second game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter third game
#     # Users finish third game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter fourth game
#     # Users finish fourth game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter fifth game
#     # Users finish fifth game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     #Assert
#     assert tcg.getUsersStreakCount(account) == 5
#     assert tcg.getUsersStreakCount(account2) == 0

# def test_winnings_calculated_correctly():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     #Arrange
#     deploy_mocks()
#     priceFeedAddress = MockV3Aggregator[-1].address
#     account = accounts[0]
#     accounts.add()
#     account2 = accounts[1]
#     KEPT_BALANCE = Web3.toWei(100, "ether")
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, priceFeedAddress, {"from": account})
#     tx = ttc.transfer(tcg.address, ttc.totalSupply() - KEPT_BALANCE, {"from": account})
#     tx.wait(1)
#     tx1 = tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     tx1.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account] = addingTransaction
#     tx2 = tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     tx2.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account2] = addingTransaction
#     tx3 = tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", users_to_transactions[account],{"from": account})
#     tx3.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account] = addingTransaction
#     tx4 = tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", users_to_transactions[account2],{"from": account})
#     tx4.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account2] = addingTransaction
#     #Act
#     tx5 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
#     tx5.wait(1)
#     tx6 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
#     tx6.wait(1)
#     tx7 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
#     tx7.wait(1)
#     tx8 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], False, 73, {"from": account})
#     tx8.wait(1)
#     tx9 = tcg.updatePlayersWins(account, account2, users_to_transactions[account], users_to_transactions[account2], True, 73, {"from": account})
#     tx9.wait(1)
#     assert tcg.getTransactionData(account, 7, {"from": account}) < 20000000000000000000
#     assert 20000000000000000000 - tcg.getTransactionData(account, 7, {"from": account}) > 20000000000000000000/2

# def test_winner_receives_correct_winnings():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     #Arrange
#     deploy_mocks()
#     priceFeedAddress = MockV3Aggregator[-1].address
#     account = accounts[0]
#     accounts.add()
#     account2 = accounts[1]
#     originalWinnerWalletAmount = account2.balance()
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, priceFeedAddress, {"from": account})
#     tx = ttc.transfer(tcg.address, ttc.totalSupply(), {"from": account})
#     tx.wait(1)
#     tx1 = tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     tx1.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account] = addingTransaction
#     tx2 = tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     tx2.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account2] = addingTransaction
#     tx3 = tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", users_to_transactions[account],{"from": account})
#     tx3.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account] = addingTransaction
#     tx4 = tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", users_to_transactions[account2],{"from": account})
#     tx4.wait(1)
#     addingTransaction = calculate_gas_price(gas_price, tx.gas_limit)
#     users_to_transactions[account2] = addingTransaction
#     #Act
#     tx5 = tcg.updatePlayersWins(account2, account, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
#     tx5.wait(1)
#     tx6 = tcg.updatePlayersWins(account2, account, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
#     tx6.wait(1)
#     tx7 = tcg.updatePlayersWins(account2, account, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
#     tx7.wait(1)
#     tx8 = tcg.updatePlayersWins(account2, account, users_to_transactions[account2], users_to_transactions[account], False, 73, {"from": account})
#     tx8.wait(1)
#     tx9 = tcg.updatePlayersWins(account2, account, users_to_transactions[account2], users_to_transactions[account], True, 73, {"from": account})
#     tx9.wait(1)
#     # Call the below function through an if statment based on the return value from tx9
#     tx10 = tcg.awardTapTapCoin(account2, {"from": account, "value": tx9.return_value})
#     tx10.wait(1)
#     #Assert
#     winningsAmount = tcg.calculateWinnings(account2, 73, {"from": account})
#     assert account2.balance() == originalWinnerWalletAmount + winningsAmount

# def test_users_games_adding_correctly():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     #Arrange
#     deploy_mocks()
#     price_feed_address = MockV3Aggregator[-1].address
#     account = accounts[0]
#     accounts.add()
#     account2 = accounts[1]
#     print("ACCOUNT 2 BELOW")
#     print(account2)
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
#     #Act
#     # Add both users wallets
#     tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE",{"from": account})
#     # Users Enter first game
#     tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
#     tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE",2186061028200000000, {"from": account})
#     # Users finish first game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter second game
#     # Users finish second game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter third game
#     # Users finish third game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter fourth game
#     # Users finish fourth game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     # Users Enter fifth game
#     # Users finish fifth game
#     tcg.updatePlayersWins(account, account2, 2186061028200000000, 2186061028200000000, False, 73, {"from": account})
#     #Assert
#     assert tcg.getUsersGamesCount(account2, {"from": account}) == 5
#     assert tcg.getUsersGamesCount(account, {"from": account}) == 5

# def test_check_wait_time_ends_correctly():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
#         pytest.skip()
#     # Arrange
#     deploy_mocks()
#     price_feed_address = MockV3Aggregator[-1].address
#     account = accounts[0]
#     accounts.add()
#     account2 = accounts[1]
#     print("ACCOUNT 2 BELOW")
#     print(account2)
#     ttc = TapTapCoin.deploy({"from": account})
#     tcg = TapCoinGame.deploy(ttc.address, price_feed_address, {"from": account})
#     tcg.addWallet(account, "TEMPORARYADDWALLETPASSCODE", {"from": account})
#     # Act
#     tcg.setUsersGamesTo100(account, {"from": account})
#     tcg.addWallet(account2, "TEMPORARYADDWALLETPASSCODE", {"from": account})
#     tcg.faceIdCheck(account2, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account})
#     time.sleep(3)
#     tcg.faceIdCheck(account, "TEMPORARYFACEIDCODE", 2186061028200000000, {"from": account})
#     # Assert
#     assert tcg.checkUserFaceIdChecked(account) == True

##################################################
##################################################
##################################################
# REVIEW THIS LATER
# test streaks are correct after multiple games
# test transactions are correct after multiple games
# test winnings are calculated correctly after multiple games
# test winner receives correct winnings after multipe games