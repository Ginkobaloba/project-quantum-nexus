# Architecture: project-quantum-nexus

**Last updated:** 2026-05-08

---

## High-level view

Quantum Nexus sits between Vector (data source) and Nexus (orchestration) in the
ecosystem. It provides specialized quantum-enhanced analytical methods that consume
sensor data and produce actionable results.

```
+-------------------+     +------------------------+     +------------------+
|  project-vector   |     | project-quantum-nexus  |     |     nexus        |
|                   |     |                        |     |                  |
| Sensor nodes      |---->| State estimation       |---->| Distributed      |
| Edge processing   |     | Anomaly detection      |     | orchestration    |
| Spatial context   |     | Energy scheduling      |     | Result routing   |
| Zone association  |     |                        |     | Action dispatch  |
+-------------------+     +------------------------+     +------------------+
        ^                          |                              |
        |                          v                              |
        |                  +----------------+                     |
        |                  | IBM Quantum    |                     |
        +------------------| Aer simulator  |---------------------+
           feedback loop   | Real hardware  |    scheduling commands
                           +----------------+
```

### Data flow (current -- simulated)

Right now, there's no live connection to Vector or Nexus. The data pipeline is:

1. `simulated_sensors.py` generates synthetic building sensor data that matches
   Vector's expected output schema (temperature, humidity, power consumption,
   occupancy, etc.)
2. `power_system_model.py` wraps that sensor data into a simplified power system
   model suitable for state estimation
3. Quantum circuits in `circuits/` process the model data
4. Results get visualized via `utils/visualization.py`

### Data flow (future -- integrated)

Once Vector's data pipeline is live and Nexus is plumbed:

1. Vector pushes real sensor data via MQTT or the Nexus message bus
2. Quantum Nexus subscribes as a Nexus service node
3. Circuits run against real data (Aer for development, IBM hardware for validation)
4. Results publish back to the Nexus bus for downstream consumers

The interface between simulated and real data should be identical -- swap the data
source, everything else stays the same. This is why `simulated_sensors.py` must
match Vector's output schema exactly.

---

## Module architecture

```
src/quantum_nexus/
|-- circuits/                 # Quantum circuit definitions
|   |-- state_estimation.py   # VQE and QAOA for power flow
|   |-- anomaly_classifier.py # Quantum kernel SVM for fault detection
|
|-- data/                     # Data generation and modeling
|   |-- simulated_sensors.py  # Synthetic sensor data (Vector-compatible)
|   |-- power_system_model.py # Power system abstraction layer
|
|-- utils/                    # Support code
    |-- visualization.py      # Plotting and result display
```

### Design principles

- **Swap-ready data layer.** The `data/` module abstracts data sources. Circuit
  code never touches raw sensor data directly -- it works through the power system
  model interface.
- **Simulator-first development.** All circuits default to Aer. Real hardware
  execution is opt-in and requires an IBM Quantum API token via environment variable.
- **Classical baselines.** Every quantum method should have a classical counterpart
  implemented alongside it. If we can't beat (or at least match) classical on the
  simulator, there's no point running on real hardware.
- **Notebook-driven demos.** Research exploration happens in notebooks. Once a
  method works, the reusable bits get refactored into `src/`.

---

## Decisions log

### ADR-001: Qiskit over Cirq/PennyLane

**Context:** Multiple quantum computing frameworks exist. Cirq (Google), PennyLane
(Xanadu), and Qiskit (IBM) are the main contenders.

**Decision:** Qiskit.

**Rationale:**
- IBM provides free access to real quantum hardware (127+ qubit processors)
- Qiskit's optimization module has built-in QAOA and VQE implementations
- Best documentation and community for applied quantum computing
- Direct path from simulator to hardware without framework changes
- PennyLane is great for quantum ML but we need optimization primitives more

**Consequences:**
- Locked to IBM hardware for real-device validation
- Qiskit's API has been volatile (the 0.x to 1.0 migration was painful)
- If Google or IonQ opens better free-tier access, we'd need to port

### ADR-002: Simulated data before real integration

**Context:** We could try to integrate with Vector's data pipeline immediately.

**Decision:** Start with simulated data.

**Rationale:**
- Vector's data pipeline isn't live yet
- Simulated data lets us control noise, completeness, and edge cases precisely
- Faster iteration -- no dependency on hardware deployment
- The interface contract (what the data looks like) is defined by Vector's schema;
  the actual source doesn't matter to the quantum circuits

**Consequences:**
- Risk of schema drift if Vector changes its output format
- Need to periodically validate that simulated data is realistic
- Integration testing gets deferred until Vector is ready
