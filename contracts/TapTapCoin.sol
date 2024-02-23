// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TapTapCoin is ERC20 {
    constructor() public ERC20("TapTap Coin", "TAPC") {
        _mint(msg.sender, 50000000000000000000000);
    }
}
