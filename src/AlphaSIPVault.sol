// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {ERC4626} from "@openzeppelin/contracts/token/ERC20/extensions/ERC4626.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";

contract AlphaSIPVault is ERC4626, ReentrancyGuard, Ownable2Step {
    using SafeERC20 for IERC20;

    uint256 public constant MAX_FEE_BPS = 200;
    uint256 public managementFeeBps;
    address public feeTreasury;

    struct Mandate {
        uint256 recurringAmount;
        uint256 intervalSeconds;
        uint256 lastExecution;
        uint256 expiry;
        bool isActive;
    }

    mapping(address => Mandate) public sipMandates;

    event SIPMandateRegistered(address indexed investor, uint256 recurringAmount, uint256 intervalSeconds, uint256 expiry);
    event SIPExecuted(address indexed investor, uint256 assetsInvested, uint256 sharesMinted);
    event MandateRevoked(address indexed investor);

    error MandateNotDue(uint256 nextDueTimestamp);
    error MandateExpired();
    error MandateInactive();
    error FeeCeilingExceeded();

    constructor(
        IERC20 asset_,
        address initialOwner,
        address feeTreasury_,
        uint256 managementFeeBps_
    ) ERC20("AlphaSIP Tokenized Vault", "asSIP") ERC4626(asset_) Ownable2Step() {
        if (managementFeeBps_ > MAX_FEE_BPS) revert FeeCeilingExceeded();
        _transferOwnership(initialOwner);
        feeTreasury = feeTreasury_;
        managementFeeBps = managementFeeBps_;
    }

    /// @notice OpenZeppelin virtual decimals offset defeats the ERC-4626 inflation attack
    function _decimalsOffset() internal view virtual override returns (uint8) {
        return 3;
    }

    function registerMandate(
        uint256 recurringAmount,
        uint256 intervalSeconds,
        uint256 expiry
    ) external {
        require(recurringAmount > 0, "Zero amount");
        require(expiry > block.timestamp + intervalSeconds, "Invalid expiry");

        sipMandates[msg.sender] = Mandate({
            recurringAmount: recurringAmount,
            intervalSeconds: intervalSeconds,
            lastExecution: block.timestamp,
            expiry: expiry,
            isActive: true
        });

        emit SIPMandateRegistered(msg.sender, recurringAmount, intervalSeconds, expiry);
    }

    function executeSIP(address investor) external nonReentrant returns (uint256 shares) {
        Mandate storage mandate = sipMandates[investor];
        if (!mandate.isActive) revert MandateInactive();
        if (block.timestamp > mandate.expiry) revert MandateExpired();
        if (block.timestamp < mandate.lastExecution + mandate.intervalSeconds) {
            revert MandateNotDue(mandate.lastExecution + mandate.intervalSeconds);
        }

        mandate.lastExecution = block.timestamp;
        IERC20(asset()).safeTransferFrom(investor, address(this), mandate.recurringAmount);

        shares = previewDeposit(mandate.recurringAmount);
        _mint(investor, shares);

        emit SIPExecuted(investor, mandate.recurringAmount, shares);
    }

    function revokeMandate() external {
        delete sipMandates[msg.sender];
        emit MandateRevoked(msg.sender);
    }
}
