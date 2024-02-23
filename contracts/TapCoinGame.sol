// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TapCoinGame is Ownable {
    IERC20 public taptapCoin;
    AggregatorV3Interface internal ethUsdPriceFeed;
    string private addWalletPassCode = "TEMPORARYADDWALLETPASSCODE";
    string private _FaceId_Code = "TEMPORARYFACEIDCODE";
    uint256 private streak_limit = 3;
    uint256 _gWinnings = 16;
    event EtherSent(address indexed recipient, uint256 amount);
    // Total transactions for each user
    struct TransactionInformation {
        uint256 addWalletTransaction;
        uint256 faceIdCheckTransaction;
        uint256 gameTransactions;
        uint256 totalTransactionAmount;
        bool hasTotalTransactions;
    }
    // Struct for keeping track of each users data throughout the game
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

    // constructor set taptapCoin and pricefeed
    constructor(address _taptapCoinAddress, address _priceFeedAddress) payable {
        taptapCoin = IERC20(_taptapCoinAddress);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function getUserStreakBoard(
        address user
    ) public view returns (TapCoinGame.streakBoardValues memory) {
        return streakBoard[user];
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
            address payable currentUserAddress = activePlayers[index];
            TapCoinGame.streakBoardValues memory currentUser = streakBoard[
                currentUserAddress
            ];
            if (currentUser.isWinner) {
                _gWinnings = setTransactionPriceForUser(currentUserAddress);
                (bool sent, ) = currentUserAddress.call{value: _gWinnings}("");
                require(sent, "Failed to send Ether");
                emit EtherSent(currentUserAddress, _gWinnings);
            }
            index++;
        }
    }

    receive() external payable {}
}
