// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TapCoinGame is Ownable {
    // IERC20 public taptapCoin
    IERC20 public taptapCoin;
    // Eth USD Price Feed
    AggregatorV3Interface internal ethUsdPriceFeed;
    // Add Wallet PassCode
    string private addWalletPassCode = "TEMPORARYADDWALLETPASSCODE";
    // RECAPTCHA PassCode
    string private _FaceId_Code = "TEMPORARYFACEIDCODE";
    // Streak limit
    uint256 private streak_limit = 3;

    uint256 _gWinnings = 16;

    address[] public addresses;

    event EtherSent(address indexed recipient, uint256 amount);

    event CheckingEvent(string _message);
    // Total transactions for each user along the way
    struct TransactionInformation {
        uint256 addWalletTransaction;
        uint256 faceIdCheckTransaction;
        uint256 gameTransactions;
        uint256 totalTransactionAmount;
        bool hasTotalTransactions;
    }
    // struct for keeping track of each users data throughout the game
    struct streakBoardValues {
        uint256 wins;
        uint256 games;
        uint256 gameIndex;
        uint waitTimeStart;
        bool faceIdCheck;
        bool isValidUser;
        bool isValidFaceId;
        bool isActive;
        bool isWinner;
        bool isAboveZero;
        bool has100Games;
        bool skipping;
        TapCoinGame.TransactionInformation transaction_info;
    }
    // mapping from user address to streakboard values for specific user
    mapping(address => TapCoinGame.streakBoardValues) public streakBoard;
    // mapping from user to index within the activePlayers array
    mapping(address => uint256) public playerIndexes;
    // array of payable active players
    address payable[] public activePlayers;

    bool public testVar = false;

    // constructor set taptapCoin and pricefeed
    constructor(address _taptapCoinAddress, address _priceFeedAddress) payable {
        taptapCoin = IERC20(_taptapCoinAddress);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function testFunction() public pure returns (string memory) {
        return "CALLING THE TEST FUNCTION IN TAPCOINGAME";
    }

    // compare two strings function for comparing the wallet and RECAPTCHA passcodes
    function compare(
        string memory str1,
        string memory str2
    ) public pure returns (bool) {
        if (bytes(str1).length != bytes(str2).length) {
            return false;
        }
        return
            keccak256(abi.encodePacked(str1)) ==
            keccak256(abi.encodePacked(str2));
    }

    // Check to make sure the address given is added to the streakboard mappings through the addWallet function
    function checkForUser(address user) public view returns (bool) {
        return streakBoard[user].isValidUser;
    }

    // Function to check that the given user has passed the RECAPTCHA
    function checkUserFaceIdChecked(address user) public view returns (bool) {
        return streakBoard[user].faceIdCheck;
    }

    // Function to check that the user is in the activePlayers array
    function checkUserIsActive(address user) public view returns (bool) {
        return streakBoard[user].isActive;
    }

    // Function to add a user to the active players array
    function addActivePlayer(address user) public returns (uint256) {
        activePlayers.push(payable(user));
        return activePlayers.length - 1;
    }

    // Function to remove user from activePlayers array after certain amount of time
    // *** CURRENTLY REMOVED FROM DEV AND MAIN ***
    function removeActivePlayer(address[] memory users) public {
        for (uint256 i = 0; i < users.length; i++) {
            if (streakBoard[users[i]].isValidUser) {
                uint256 index = playerIndexes[users[i]];
                uint256 lastPlayerIndex = activePlayers.length - 1;
                address lastPlayer = activePlayers[lastPlayerIndex];
                address playerToBeRemoved = activePlayers[index];
                // we brought the last item to the index that we remove.
                // we end up [1,2,5,4,5]
                activePlayers[index] = payable(lastPlayer);
                // update the mapping. now in mapping id5 should be 2nd index
                playerIndexes[users[i]] = index; // {1:0,2:1,3:2,4:3,5:2}
                delete playerIndexes[playerToBeRemoved];
                activePlayers.pop();
            }
        }
    }

    function get_test_var() public view returns (bool) {
        return testVar;
    }

    // Function to check that the wait time is done for a user who is over 100 games
    // Returns true if wait time is done or users has not reach 100 games yet
    // Returns false if wait time is still active
    function checkWaitTimeIsDone(address user) internal returns (bool) {
        // uint oneDay = 86400;
        uint testOneDay = 1;
        if (!streakBoard[user].has100Games) {
            return true;
        }
        if (block.timestamp >= (streakBoard[user].waitTimeStart + testOneDay)) {
            streakBoard[user].has100Games = false;
            streakBoard[user].games = 0;
            return true;
        }
        return false;
    }

    // Function to check if the users have played their 100th game in a row
    // *** CURRENTLY REMOVED FROM DEV AND MAIN ***
    function checkOneHundredGames(address winner, address loser) internal {
        if (streakBoard[winner].games == 100) {
            streakBoard[winner].has100Games = true;
            streakBoard[winner].waitTimeStart = block.timestamp;
        }
        if (streakBoard[loser].games == 100) {
            streakBoard[loser].has100Games = true;
            streakBoard[loser].waitTimeStart = block.timestamp;
        }
    }

    // Function to set each of the transaction prices for a user
    // And the totalTransaction price
    function setTransactionPriceForUser(
        address user_address
    ) internal view returns (uint256) {
        TapCoinGame.streakBoardValues memory user = streakBoard[user_address];
        uint256 totalAmount = user.transaction_info.addWalletTransaction +
            user.transaction_info.faceIdCheckTransaction +
            user.transaction_info.gameTransactions;
        user.transaction_info.totalTransactionAmount = totalAmount;
        user.transaction_info.hasTotalTransactions = true;
        return totalAmount;
    }

    function returnWinningsAmount() public view returns (uint256) {
        return _gWinnings;
    }

    // Function to get the total TapTapCoin supply left in TapCoinGame
    function getTotalTapTapCoinSupply() public view returns (uint256) {
        return taptapCoin.totalSupply();
    }

    function getTotalContractAmount() public view returns (uint256) {
        return address(this).balance;
    }

    // Function to get the current actual USD one cent price based off the eth_usd_price_feed
    function getCurrentActualUsdOneCentCost() public view returns (uint256) {
        uint256 oneUSDCent = 1 * 10 ** 16;
        uint256 precision = 1 * 10 ** 18;
        uint256 price = getPrice();
        return (oneUSDCent * precision) / price;
    }

    // Function to get the current price of ETH
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = ethUsdPriceFeed.latestRoundData();
        // ETH/USD rate in 18 digit
        return uint256(answer * 10000000000);
    }

    // Function for adding a new users address to the game
    // Will also set the streakboard values for to their starting values
    // As well as adding users to active players array
    function addWallet(
        address newAccount,
        string memory code
    ) public returns (address payable[] memory) {
        // Figure out how to connect a wallet
        // Do this later most likely
        // save address in db as well
        string memory _code = addWalletPassCode;
        require(compare(code, _code), "This is not a valid transaction");
        // require that the newAccount being added is not already added ( may be dealing with the revert bugg )
        streakBoard[newAccount].wins = 0;
        streakBoard[newAccount].isValidUser = true;
        streakBoard[newAccount].isActive = true;
        streakBoard[newAccount].faceIdCheck = false;
        // Adjust add wallet transaction
        streakBoard[newAccount]
            .transaction_info
            .addWalletTransaction = getCurrentActualUsdOneCentCost();
        streakBoard[newAccount].transaction_info.faceIdCheckTransaction = 0;
        streakBoard[newAccount].transaction_info.gameTransactions = 0;
        streakBoard[newAccount].has100Games = false;
        uint256 newIndex = addActivePlayer(newAccount);
        playerIndexes[newAccount] = newIndex;
        return activePlayers;
    }

    // Function for updating the passed RECAPTCHA mapping for a user
    function faceIdCheck(
        address user,
        string memory code,
        uint256 transaction_price
    ) public returns (TapCoinGame.streakBoardValues memory) {
        // DEV Side
        // addWallet(user, "TEMPORARYADDWALLETPASSCODE");
        string memory _code = _FaceId_Code;
        // validate address is present
        require(checkForUser(user) == true, "This account is not registered.");
        // validate user is active
        require(checkUserIsActive(user) == true, "This account is not active.");
        // validate RECAPTCHA passCode
        require(compare(code, _code), "This is not a valid transaction");
        // validate that the users are not on the 24 hour wait time
        require(
            checkWaitTimeIsDone(user) == true,
            "This account is not allowed to play at this time."
        );
        // update RECAPTCHA value to address
        streakBoard[user].faceIdCheck = true;
        // update RECAPTCHA transaction for user
        streakBoard[user]
            .transaction_info
            .faceIdCheckTransaction = transaction_price;
        streakBoard[user].skipping = false;
        streakBoard[user].gameIndex = 0;
        return streakBoard[user];
    }

    // Function for updating the wins for two users and checking if a user has reached the streak_limit
    function updatePlayersWins(
        address winner,
        address loser,
        uint256 transaction_price_winner,
        uint256 transaction_price_loser,
        uint256 percentage
    ) public returns (uint256) {
        require(
            checkForUser(winner) == true,
            "The Winning account is not registered."
        );
        require(
            checkForUser(loser) == true,
            "The Losing account is not registered."
        );
        // validate users are active
        require(
            checkUserIsActive(winner) == true,
            "The Winning account is not active."
        );
        require(
            checkUserIsActive(loser) == true,
            "The Losing account is not active."
        );
        // validate that the RECAPTCHA has been passed for both users
        require(
            checkUserFaceIdChecked(winner) == true,
            "The Winning account does not have a valid RECAPTCHA."
        );
        require(
            checkUserFaceIdChecked(loser) == true,
            "The Losing account does not have a valid RECAPTCHA."
        );
        // validate that the users are not on the 24 hour wait time
        require(
            checkWaitTimeIsDone(winner),
            "The Winning account is not allowed to play at this time."
        );
        require(
            checkWaitTimeIsDone(loser),
            "The Losing account is not allowed to play at this time."
        );
        testVar = true;
        streakBoard[winner].transaction_info.hasTotalTransactions = false;
        streakBoard[loser].transaction_info.hasTotalTransactions = false;
        // adjust both users wins. If winner add 1 if lost set to 0
        streakBoard[winner].wins += 1;
        streakBoard[loser].wins = 0;
        // adjust games of both users plus one regardless
        streakBoard[winner].games += 1;
        streakBoard[loser].games += 1;
        // set a boolean variable to recognize who is the winner
        streakBoard[winner].isWinner = true;
        streakBoard[loser].isWinner = false;
        streakBoard[winner]
            .transaction_info
            .gameTransactions += transaction_price_winner;
        streakBoard[loser]
            .transaction_info
            .gameTransactions += transaction_price_loser;
        return 1;
    }

    // Function for awarding taptapCoin to a winner
    function awardTapTapCoin() public payable {
        require(address(this).balance >= 0, "Insufficient contract balance");
        // Make onlyowner
        // set up requires to checek it is a valid winner
        // call Function to figure out winnings
        // award coin from my account to winners account
        // streakBoard[winner].totalTransactions = 0; // set function to reset losers after a certain amount of time so the transactions don't persist for long periods of time
        uint256 activePlayersLength = activePlayers.length;
        uint256 index = 0;
        while (index != activePlayersLength) {
            address payable currentWinner = activePlayers[index];
            index++;
            _gWinnings = setTransactionPriceForUser(currentWinner);
            (bool sent, ) = currentWinner.call{value: _gWinnings}("");
            require(sent, "Failed to send Ether");
            // currentWinner.transfer(10000000000000000);
            emit EtherSent(currentWinner, _gWinnings);
        }
        // require(amount > 0, "Amount must be greater than zero");
    }

    receive() external payable {}
}

// DEV Side
// addWallet(winner, "TEMPORARYADDWALLETPASSCODE");
// addWallet(loser, "TEMPORARYADDWALLETPASSCODE");
// faceIdCheck(
//     winner,
//     "TEMPORARYFACEIDCODE",
//     10000000000000000000000000000000000
// );
// faceIdCheck(
//     loser,
//     "TEMPORARYFACEIDCODE",
//     10000000000000000000000000000000000
// );
// streakBoard[winner].wins += 1;
// streakBoard[winner].wins += 1;
// streakBoard[winner].wins += 1;
// streakBoard[winner].wins += 1;
// // adjust games of both users plus one regardless
// streakBoard[winner].games += 1;
// streakBoard[loser].games += 1;
// streakBoard[winner].games += 1;
// streakBoard[loser].games += 1;
// streakBoard[winner].games += 1;
// streakBoard[loser].games += 1;
// streakBoard[winner].games += 1;
// streakBoard[loser].games += 1;
// streakBoard[winner]
//     .totalTransactions
//     .transaction_1 = 10000000000000000000000000000000000;
// streakBoard[winner]
//     .totalTransactions
//     .transaction_2 = 10000000000000000000000000000000000;
// streakBoard[winner]
//     .totalTransactions
//     .transaction_3 = 10000000000000000000000000000000000;
// streakBoard[winner]
//     .totalTransactions
//     .transaction_4 = 10000000000000000000000000000000000;
// streakBoard[loser]
//     .totalTransactions
//     .transaction_1 = 10000000000000000000000000000000000;
// streakBoard[loser]
//     .totalTransactions
//     .transaction_2 = 10000000000000000000000000000000000;
// streakBoard[loser]
//     .totalTransactions
//     .transaction_3 = 10000000000000000000000000000000000;
// streakBoard[loser]
//     .totalTransactions
//     .transaction_4 = 10000000000000000000000000000000000;
// validate that the users wallets are present

// Update Players Wins Extra Code
// if (streakBoard[winner].gameIndex == 0) {
//     streakBoard[winner]
//         .totalTransactions
//         .transaction_1 = transaction_price_winner;
// } else if (streakBoard[winner].gameIndex == 1) {
//     streakBoard[winner]
//         .totalTransactions
//         .transaction_2 = transaction_price_winner;
// } else if (streakBoard[winner].gameIndex == 2) {
//     streakBoard[winner]
//         .totalTransactions
//         .transaction_3 = transaction_price_winner;
// }
// streakBoard[winner].totalTransactions.totalTransactionAmount =
//     streakBoard[winner].totalTransactions.transaction_1 +
//     streakBoard[winner].totalTransactions.transaction_2 +
//     streakBoard[winner].totalTransactions.transaction_3;
// // streakBoard[user].totalTransactions.transaction_4 +
// // streakBoard[user].totalTransactions.transaction_5;
// streakBoard[winner].totalTransactions.hasTotalTransactions = true;
// if (streakBoard[loser].gameIndex == 0) {
//     streakBoard[loser]
//         .totalTransactions
//         .transaction_1 = transaction_price_loser;
// } else if (streakBoard[loser].gameIndex == 1) {
//     streakBoard[loser]
//         .totalTransactions
//         .transaction_2 = transaction_price_loser;
// } else if (streakBoard[loser].gameIndex == 2) {
//     streakBoard[loser]
//         .totalTransactions
//         .transaction_3 = transaction_price_loser;
// }
// streakBoard[loser].totalTransactions.totalTransactionAmount =
//     streakBoard[loser].totalTransactions.transaction_1 +
//     streakBoard[loser].totalTransactions.transaction_2 +
//     streakBoard[loser].totalTransactions.transaction_3;
// // streakBoard[loser].totalTransactions.transaction_4 +
// // streakBoard[loser].totalTransactions.transaction_5;
// streakBoard[loser].totalTransactions.hasTotalTransactions = true;
// streakBoard[loser].gameIndex += 1;
// streakBoard[loser].gameIndex += 1;

// if (streakBoard[winner].gameIndex == 3) {
//     streakBoard[winner].gameIndex = 0;
// }
// if (streakBoard[loser].gameIndex == 3) {
//     streakBoard[loser].gameIndex = 0;
// }
// Send event as a message figure this out later
// if winner passed streak limit then award coin
// if (streakBoard[winner].wins >= streak_limit) {
//     // calculate the transactions prices of the users respectivley
//     // calculateGames(winner, transaction_price_winner);
//     // calculateGames(loser, transaction_price_loser);
//     // // // set RECAPTCHA values back to false
//     streakBoard[winner].faceIdCheck = false;
//     streakBoard[loser].faceIdCheck = false;
//     // Set up sending active users information from frontend side to blockchain
//     uint256 winnings = calculateWinnings(winner, percentage);
//     _gWinnings = winnings;
//     checkOneHundredGames(winner, loser);
//     awardTapTapCoin(winner);
//     return winnings;
// }
// checkOneHundredGames(winner, loser);

// function send_winnings_to_users(address winner) public returns (bool) {
//     // set boolean in updatePlayerWins for if a user has a 3 game win streak or not
//     // loop through all users and check if users has a win streak
//     // if user has a win streak then calculate games for that users winnings (get user from payable array)
//     // then adjust any booleans for that users
//     // then check oneHundred games
//     // then award tapcoin to user
//     // continue through loop
//     awardTapTapCoin(winner);
// }

// Function to use the number of games of a user to see what their
// Transaction prices are and their totalTransaction cost
// function calculateGames(address user, uint256 transaction_price) internal {
//     uint256 numberOfGames = streakBoard[user].games;
//     uint256 gameIndex = 0;
//     // if the skip is set to false, which it should be for the first 5 games
//     // then continue
//     if (!streakBoard[user].skipping) {
//         // if the number of games is less than 6
//         // then it is the first 5 games and the
//         // first 5 transactions still need to be set
//         // set the game index to 1 minus the number of
//         // games played.
//         if (numberOfGames < 6) {
//             gameIndex = numberOfGames - 1;
//         }
//         // if the number of games is greater than 9
//         // then it is after 5 more games than the initial
//         // 5 games for the first 5 transactions
//         else if (numberOfGames > 9) {
//             // Every 5 games reset gameIndex to 0 and invalidate current RECAPTCHA
//             if (numberOfGames % 5 == 0) {
//                 gameIndex = 0;
//                 streakBoard[user].faceIdCheck = false;
//             }
//             // Increase gameIndex by 1 to set the next transaction price
//             else {
//                 gameIndex += 1;
//             }
//         }
//         // if less than or equal to 9 but greater than or equal to 6 games
//         // skip the rest of the functionality and keep the current total
//         // transactions for 5 games.
//         else {
//             streakBoard[user].skipping = true;
//         }
//         // if everything passes and it is not skipping
//         // then set the transaction price based on the
//         // gameindex and the transaction_price passed
//         if (!streakBoard[user].skipping) {
//             setTransactionPriceForUser(user);
//         }
//     }
//     // if skip is set to true, which should only be for games 6 - 9,
//     // then check if the next game is game 10 and if it is
//     // then set the skip back to false
//     else if ((streakBoard[user].games + 1) % 5 == 0) {
//         streakBoard[user].skipping = false;
//     }
// }

// DELETE???
// function getConversion(address user) public view returns (uint256) {
//     return getTransactionData(user, 7) / getCurrentActualUsdCost();
// }

// Function to figure out the winnings based off:
// The percentage of currently active users
// The total transaction price of the user
// function calculateWinnings(
//     address winner,
//     uint256 percentage
// ) public view returns (uint256) {
//     require(
//         streakBoard[winner].transaction_info.hasTotalTransactions == true,
//         "You do not have a valid transaction amount to calculate the winnings."
//     );
//     uint256 tranBaseLine = streakBoard[winner]
//         .transaction_info
//         .totalTransactionAmount;
//     uint256 READBaseLine = streakBoard[winner]
//         .transaction_info
//         .addWalletTransaction +
//         streakBoard[winner].transaction_info.faceIdCheckTransaction;
//     uint256 winningsBaseLine = tranBaseLine + READBaseLine;
//     uint256 winnings = factor_active_players_percentage(
//         winningsBaseLine,
//         percentage
//     );
//     return winnings;
// }

// Function for factoring the active players percentage into
// The total winnings amount
// function factor_active_players_percentage(
//     uint256 winnings,
//     uint256 percentage
// ) internal pure returns (uint256) {
//     uint256 percantageWithDecimals = percentage * 10 ** 16;
//     return winnings / percantageWithDecimals;
// }

// Function to get a specfic piece of transaction data
// function getTransactionData(
//     address user,
//     uint256 dataIndex
// ) public view returns (uint256) {
//     if (dataIndex == 0) {
//         return streakBoard[user].transaction_info.addWalletTransaction;
//     } else if (dataIndex == 1) {
//         return streakBoard[user].transaction_info.faceIdCheckTransaction;
//     }
//     // else if (dataIndex == 2) {
//     //     return streakBoard[user].totalTransactions.transaction_1;
//     // } else if (dataIndex == 3) {
//     //     return streakBoard[user].totalTransactions.transaction_2;
//     // } else if (dataIndex == 4) {
//     //     return streakBoard[user].totalTransactions.transaction_3;
//     // }
//     // else if (dataIndex == 5) {
//     //     return streakBoard[user].totalTransactions.transaction_4;
//     // } else if (dataIndex == 6) {
//     //     return streakBoard[user].totalTransactions.transaction_5;
//     // }
//     else if (dataIndex == 7) {
//         return streakBoard[user].transaction_info.totalTransactionAmount;
//     }
// }

// DELETE???
// function getCurrentActualUsdCost() public view returns (uint256) {
//     uint256 oneUSD = 1 * 10 ** 18;
//     uint256 precision = 1 * 10 ** 18;
//     uint256 price = getPrice();
//     return (oneUSD * precision) / price;
// }

// DELETE???
// function testCalculateWinnings(
//     address winner
// ) public view returns (uint256) {
//     uint256 totalTransactions = this.getTransactionData(winner, 7);
//     uint256 oneUSD = 1 * 10 ** 18;
//     uint256 precision = 1 * 10 ** 18;
//     uint256 price = getPrice();
//     uint256 currentActualUsdCost = (oneUSD * precision) / price;
//     if (totalTransactions > currentActualUsdCost) {
//         return 0;
//     } else {
//         return 1;
//     }
// }

// Function to get the given users current win count
// function getUsersStreakCount(address user) public view returns (uint256) {
//     return streakBoard[user].wins;
// }

// function getUserStreakBoard(
//     address user
// ) public view returns (TapCoinGame.streakBoardValues memory) {
//     return streakBoard[user];
// }

// Function to get the given users game count
// function getUsersGamesCount(address user) public view returns (uint256) {
//     return streakBoard[user].games;
// }

// function setUsersGamesTo100(address user) public {
//     streakBoard[user].games = 100;
//     streakBoard[user].has100Games = true;
//     streakBoard[user].waitTimeStart = block.timestamp;
// }
