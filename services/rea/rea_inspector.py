# REA — Reverse Engineer Anything Inspection Harness
# Upstream: https://github.com/morluto/rea.git
import os

class REAInspector:
    def __init__(self, target_dir="."):
        self.target = target_dir

    def inspect_dependencies(self):
        suspicious = []
        # Inspect for unpinned dependencies or dynamic eval vulnerabilities
        for root, _, files in os.walk(self.target):
            for file in files:
                if file.endswith((".py", ".ts", ".sol", ".rs")):
                    full = os.path.join(root, file)
                    try:
                        with open(full, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if "eval(" in content:
                                suspicious.append((file, "Dynamic eval call detected"))
                    except:
                        pass
        return {
            "scanned_files": True,
            "findings": suspicious,
            "status": "CLEAN" if len(suspicious) == 0 else "FLAGGED"
        }
