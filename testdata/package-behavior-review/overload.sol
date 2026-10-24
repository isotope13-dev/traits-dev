pragma solidity ^0.8.17;
contract Reader { function read(address target, bytes memory data) internal view { read(target, data, bytes4(0), ""); } function read(address target, bytes memory data, bytes4 cb, bytes memory extra) internal view { target.staticcall(data); } }
