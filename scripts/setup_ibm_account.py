"""
One-time setup: saves IBM Quantum credentials from .env to ~/.qiskit/ config.

Run this once per machine:
    python scripts/setup_ibm_account.py

After that, QiskitRuntimeService() works without arguments.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

token = os.getenv("IBM_QUANTUM_API_KEY")
if not token:
    print("ERROR: IBM_QUANTUM_API_KEY not found in .env")
    sys.exit(1)

instance = os.getenv("IBM_INSTANCE_CRN")  # optional CRN

kwargs: dict = {"channel": "ibm_quantum_platform", "token": token, "overwrite": True}
if instance:
    kwargs["instance"] = instance

QiskitRuntimeService.save_account(**kwargs)
print("IBM Quantum account saved. QiskitRuntimeService() will now work without arguments.")
