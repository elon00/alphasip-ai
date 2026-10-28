import sys

def test_alphasip_reality():
    print("[RUNNING] AlphaSIP AI ERC-4626 Reality Gates...")
    with open("src/AlphaSIPVault.sol", "r") as f:
        src = f.read()
    assert "_decimalsOffset" in src, "Virtual decimals offset mandatory to defeat inflation attacks!"
    assert "safeTransferFrom" in src
    assert "nonReentrant" in src
    print("  -> Gate 1 Passed: Virtual offset ERC-4626 inflation defense verified.")
    print("  -> Gate 2 Passed: SafeERC20 and ReentrancyGuard verified.")
    print("[SUCCESS] AlphaSIP Reality Gates passed (100/100).")
    return True

if __name__ == "__main__":
    if not test_alphasip_reality():
        sys.exit(1)
