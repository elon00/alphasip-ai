# Automated Sanity Test Harness
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import base64
import json
import time

def run_sanity_test():
    print("[SANITY TEST] Validating single transactional lifecycle...")
    try:
        from services.x402.bazaar_gateway import X402BazaarGateway
        from services.tokenomics.uncapped_launchpad import UncappedTokenomicsEngine
        from services.wallets.qr_multiconnect import QRMultiwalletEngine

        # Test x402 payment proof verification
        gw = X402BazaarGateway("res_test", "500000", "0xTestVault")
        ch = gw.create_402_challenge()
        proof_payload = {
            "nonce": ch["nonce"],
            "expiresAt": ch["expiresAt"],
            "txHash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        }
        proof_str = base64.b64encode(json.dumps(proof_payload).encode('utf-8')).decode('utf-8')
        valid, msg = gw.verify_proof(proof_str, ch["nonce"])
        assert valid, f"Sanity proof verification failed: {msg}"

        # Test Tokenomics mint & burn
        tok = UncappedTokenomicsEngine(1_000_000)
        res = tok.execute_mint_and_burn(10_000, 2_000)
        assert res["circulating"] == 1_008_000, "Tokenomics accounting mismatch"

        # Test QR generation
        qr = QRMultiwalletEngine("base")
        uri = qr.generate_payment_uri("0xUser", "1000000")
        assert "ethereum:0xUser" in uri, "QR URI malformed"

        print("  -> Sanity Test: Single-quote, single-mint, and payment flow verified.")
        return True
    except Exception as e:
        print(f"  -> SANITY TEST FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    if not run_sanity_test():
        sys.exit(1)
