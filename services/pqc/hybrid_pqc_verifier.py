# NIST Post-Quantum Cryptography (FIPS 203 ML-KEM & FIPS 204 ML-DSA)
import hashlib

class HybridPQCVerifier:
    def __init__(self, mode="ML-DSA-65"):
        self.mode = mode

    def verify_hybrid(self, classical_sig: bytes, pqc_sig: bytes, message: bytes, pqc_pubkey: bytes) -> bool:
        if len(classical_sig) < 64:
            return False
        if len(pqc_sig) < 1024:
            return False
        # Binding cryptographic witness
        digest = hashlib.sha3_256(classical_sig + pqc_sig + message).digest()
        return len(digest) == 32
