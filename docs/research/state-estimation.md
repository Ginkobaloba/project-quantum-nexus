# Quantum Approaches to Power System State Estimation

**Status:** Research notes, not a paper. Updated 2026-05-08.

---

## What is state estimation?

Power system state estimation (SE) takes a bunch of noisy, incomplete sensor
measurements (voltage magnitudes, power flows, current injections) and figures out
the most likely actual state of the network. It's basically a large nonlinear
optimization problem.

The classical workhorse is Weighted Least Squares (WLS), which minimizes the
weighted residuals between measured and estimated values. Works fine for small
networks. Starts sweating when you scale up to hundreds or thousands of buses with
real-time constraints.

## Why quantum?

Two angles:

### 1. Variational Quantum Eigensolver (VQE) formulation

The SE problem can be reformulated as finding the ground state of a cost Hamiltonian.
The cost function (sum of weighted squared residuals) maps to a Hamiltonian whose
ground state encodes the optimal state estimate.

VQE uses a parameterized quantum circuit (ansatz) and classical optimization to find
this ground state. The quantum advantage claim is that the parameterized circuit can
explore the solution space more efficiently than classical solvers for certain
problem structures.

**Relevant Qiskit tools:**
- `qiskit.circuit.library.EfficientSU2` -- good default ansatz
- `qiskit_algorithms.VQE` -- the VQE solver itself
- `qiskit_algorithms.optimizers` -- classical optimizers (COBYLA, SPSA, L-BFGS-B)
- `qiskit_aer.AerSimulator` -- for development and testing

### 2. QAOA for combinatorial subproblems

Some aspects of SE involve discrete decisions (which measurements to trust, topology
estimation, bad data detection). These map naturally to QAOA.

**Relevant Qiskit tools:**
- `qiskit_optimization.algorithms.QAOA` -- QAOA solver
- `qiskit_optimization.applications` -- problem formulation helpers
- `qiskit_optimization.converters.QuadraticProgramToQubo` -- QUBO conversion

## How this connects to the ecosystem

- **Vector** generates the sensor measurements. In real deployment, these would be
  temperature, humidity, power consumption, and occupancy readings from building
  sensor nodes. For SE, we care primarily about electrical measurements.
- **Quantum Nexus** (this project) runs the quantum-enhanced SE algorithm.
- **Nexus** could distribute the SE computation across multiple nodes, each handling
  a subsystem of the network.

The patent ecosystem boundary: the quantum SE method itself is open research (MIT
licensed). The specific sensor data schemas and zone-association logic that generate
the measurements are part of Vector's patent.

## Approach for the demo

1. Build a simple power system model (5-14 bus IEEE test case)
2. Generate synthetic measurements with known noise characteristics
3. Implement classical WLS as the baseline
4. Implement VQE-based SE
5. Compare accuracy and computational cost
6. Scale up and see where (if) quantum starts to help

The IEEE 14-bus system is the "hello world" of power system analysis. Small enough
to simulate quickly, complex enough to be non-trivial.

## Open questions

- **Ansatz selection:** EfficientSU2 is the default, but the optimal ansatz for SE
  problems is an open research question. Hardware-efficient ansatzes vs.
  problem-inspired ansatzes -- worth exploring both.
- **Noise resilience:** Real quantum hardware is noisy. How much does noise degrade
  the SE estimate compared to WLS? Error mitigation techniques (ZNE, PEC) might help.
- **Scaling:** VQE's classical optimization loop can get stuck in local minima for
  larger problems. Is there a practical crossover point where quantum helps?
- **Hybrid approach:** Maybe the optimal strategy is quantum for the hardest
  subproblems and classical for the rest. Need to identify which subproblems benefit
  most.

## Key references

- Eskandarpour, R., et al. "Quantum computing for power systems analysis." (2022)
- Feng, Y., et al. "Quantum computing for energy systems optimization." (2023)
- IBM Qiskit textbook, VQE chapter
- IEEE 14-bus test case data (standard benchmark)

## Next steps

1. Implement the IEEE 14-bus model in `power_system_model.py`
2. Build the WLS classical baseline
3. Formulate the cost Hamiltonian
4. Implement VQE-based solver in `state_estimation.py`
5. Run comparison in `02_state_estimation_demo` notebook
