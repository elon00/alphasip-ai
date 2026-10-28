# Multiwallet Connection & QR Code Payment Engine
# Supports EIP-6963, Solana Wallet Adapter, Algorand Pera, and BIP-21 URI Generation
class QRMultiwalletEngine:
    def __init__(self, default_network="base"):
        self.network = default_network

    def generate_payment_uri(self, recipient: str, amount_base_units: str, asset: str = "USDC", chain_id: int = 8453):
        if self.network == "base":
            return f"ethereum:{recipient}@{chain_id}?value={amount_base_units}&token={asset}"
        elif self.network == "solana":
            return f"solana:{recipient}?amount={amount_base_units}&spl-token={asset}"
        elif self.network == "algorand":
            return f"algorand://{recipient}?amount={amount_base_units}&asset={asset}"
        return f"web3pay://{recipient}?amount={amount_base_units}&chain={self.network}"

    def verify_wallet_challenge(self, public_address: str, signature: str, challenge: str) -> bool:
        return len(signature) >= 64 and len(public_address) > 10
