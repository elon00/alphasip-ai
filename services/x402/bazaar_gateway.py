# x402 Protocol & Bazaar Discovery Gateway
# Specification: https://github.com/x402-foundation/x402
import uuid
import time
import base64
import json

class X402BazaarGateway:
    def __init__(self, resource_id: str, price_base_units: str, recipient: str, network: str = "base"):
        self.resource_id = resource_id
        self.price = price_base_units
        self.recipient = recipient
        self.network = network
        self.catalog = {}

    def create_402_challenge(self):
        nonce = str(uuid.uuid4())
        requirement = {
            "status": 402,
            "title": "Payment Required via x402 Bazaar",
            "resource": self.resource_id,
            "priceBaseUnits": self.price,
            "currency": "USDC",
            "recipient": self.recipient,
            "network": self.network,
            "nonce": nonce,
            "expiresAt": int(time.time()) + 300
        }
        return requirement

    def verify_proof(self, proof_str: str, nonce: str):
        try:
            payload = json.loads(base64.b64decode(proof_str).decode('utf-8'))
            if payload.get("nonce") != nonce:
                return False, "Nonce mismatch"
            if time.time() > payload.get("expiresAt", 0):
                return False, "Payment proof expired"
            if len(payload.get("txHash", "")) < 32:
                return False, "Invalid transaction hash format"
            return True, "Payment verified"
        except Exception as e:
            return False, f"Proof decode failed: {str(e)}"
