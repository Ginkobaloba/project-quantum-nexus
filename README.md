# project-quantum-nexus

Quantum-enhanced computational methods for distributed power system intelligence.

**Status:** Early scaffold. Nothing runs yet. If you're reading this expecting a working quantum advantage, come back in a few months.

**License:** MIT

---

## What this is

This project explores whether near-term quantum computing (NISQ-era hardware, IBM's open-access backends via Qiskit) can provide meaningful analytical advantages for power system problems -- specifically the kinds of problems that show up in distributed building management and grid-edge intelligence.

Three focus areas:

- **State estimation** -- using variational quantum eigensolvers and quantum-enhanced optimization to solve power flow equations that scale poorly on classical hardware
- **Anomaly detection** -- quantum kernel methods and parameterized quantum circuits for classifying sensor data patterns that indicate faults, intrusions, or degradation
- **Energy scheduling** -- quantum approximate optimization (QAOA) for combinatorial scheduling problems in distributed energy resources

All of this runs against simulated sensor data and simplified power system models. No real buildings were harmed in the making of this code.

---

## How this connects to the other projects

This sits alongside two other projects under `C:\dev\`:

### project-vector

The autonomous mobile perception platform for building management. Has a provisional patent covering its zone-association engine, spatial intelligence layer, and autonomous navigation approach. Vector generates the kind of sensor data and spatial context that quantum-nexus methods would eventually consume.

**Relationship:** quantum-nexus provides analytical methods that could enhance Vector's anomaly detection and predictive capabilities. The patent ecosystem defines what can be open-sourced (quantum methods = MIT, Vector-specific integrations = protected).

### nexus (distributed AI architecture)

The distributed intelligence framework -- nodes, runtimes, message routing, the whole orchestration layer. Nexus is the nervous system; quantum-nexus provides specialized analytical "organs" that plug into it.

**Relationship:** quantum-nexus modules are designed to be deployable as Nexus service nodes. The circuit definitions and optimization routines wrap into standard Nexus interfaces.

### The triangle

```
    project-vector (perception + data)
           |
           | sensor data, spatial context
           v
    project-quantum-nexus (analytical methods)
           |
           | optimized results, classifications
           v
    nexus (orchestration + distribution)
```

Vector feeds data. Quantum-nexus crunches it. Nexus distributes the results. Each project is independently useful, but together they form a coherent research platform.

---

## Environment

- **Python 3.10+**
- **Qiskit 1.0+** with Aer simulator and optimization modules
- **Target hardware:** IBM open-access quantum backends (ibm_brisbane, ibm_osaka, etc.)
- **Current mode:** Simulated. All demos run on Aer simulator by default.

### Setup

```bash
# Clone
git clone https://github.com/Ginkobaloba/project-quantum-nexus.git
cd project-quantum-nexus

# Virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

---

## Project structure

```
project-quantum-nexus/
|-- README.md
|-- CLAUDE.md                    # AI session instructions
|-- LICENSE                      # MIT
|-- pyproject.toml
|-- requirements.txt
|-- docs/
|   |-- architecture.md          # System architecture and design decisions
|   |-- research/
|   |   |-- state-estimation.md  # VQE/QAOA for power flow
|   |   |-- anomaly-detection.md # Quantum kernels for fault detection
|   |   |-- energy-scheduling.md # QAOA for DER scheduling
|   |-- handoffs/
|       |-- template.md          # Session handoff template
|-- src/quantum_nexus/
|   |-- circuits/                # Quantum circuit definitions
|   |   |-- state_estimation.py
|   |   |-- anomaly_classifier.py
|   |-- data/                    # Simulated data generation
|   |   |-- simulated_sensors.py
|   |   |-- power_system_model.py
|   |-- utils/                   # Visualization and helpers
|       |-- visualization.py
|-- notebooks/                   # Demo scripts (placeholder .py files)
|-- tests/
```

---

## Session protocol

This project follows the `C:\dev\SESSION_PROTOCOL.md` cross-device session protocol. Every work session starts with `vstart` and ends with `vend` + a handoff doc. See the protocol for details.

---

## Contributing

This is a personal research project. If you're interested in quantum methods for power systems, open an issue and let's talk. PRs welcome if they come with tests.

---

## Acknowledgments

Built on [Qiskit](https://qiskit.org/) by IBM. Quantum hardware access via IBM Quantum Platform.
