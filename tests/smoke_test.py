# Automated Smoke Test Harness (< 5s Execution)
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_smoke_test():
    print("[SMOKE TEST] Verifying critical path availability...")
    try:
        from services.quicknode.provider import QuickNodeProvider
        from services.x402.bazaar_gateway import X402BazaarGateway
        from services.conway.automaton_engine import ConwayAutomatonEngine

        # QuickNode health
        qn = QuickNodeProvider()
        assert qn.verify_health(), "QuickNode RPC health check failed"

        # x402 Challenge
        x402 = X402BazaarGateway("res_01", "1000000", "0xVault")
        ch = x402.create_402_challenge()
        assert ch["status"] == 402, "x402 challenge failed"

        # Conway Step
        conway = ConwayAutomatonEngine(8, 8)
        conway.set_cell(1, 1, 1)
        h = conway.step()
        assert len(h) == 64, "Conway state hash invalid"

        print("  -> Smoke Test: All services reachable and initialized.")
        return True
    except Exception as e:
        print(f"  -> SMOKE TEST FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    if not run_smoke_test():
        sys.exit(1)
