pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TapTapCoin is ERC20 {
    constructor() public ERC20("TapTap Coin", "TAPC") {
        _mint(msg.sender, 50000000000000000000000);
    }
    // approve()
    // decreaseAllowance()
    // increaseAllowance()
    // transfer()
    // transferFrom()
    // allowance()
    // balanceOf()
    // decimals()
    // name()
    // symbol()
    // totalSupply()

    // mintFunction()
}
