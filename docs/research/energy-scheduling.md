# Quantum Optimization for Energy-Aware Distributed Compute Scheduling

**Status:** Research notes. Updated 2026-05-08.

---

## The problem

You have a building (or a campus, or a grid edge) with distributed compute
resources -- edge processors, local servers, sensor gateways. Each has different
power consumption profiles, thermal constraints, and computational capabilities.
You also have a set of computational tasks with deadlines, priority levels, and
resource requirements.

The question: how do you schedule those tasks across those resources to minimize
total energy consumption while meeting all deadlines?

This is a combinatorial optimization problem. Specifically, it's a variant of the
job-shop scheduling problem with energy as the objective function. Classical
approaches (integer linear programming, heuristic search, genetic algorithms) work
but don't scale gracefully. As you add resources and tasks, the solution space
explodes combinatorially.

This is arguably the strongest candidate for near-term quantum advantage in the
whole ecosystem. QAOA was literally designed for this class of problem.

## Why QAOA?

Quantum Approximate Optimization Algorithm (QAOA) finds approximate solutions to
combinatorial optimization problems by encoding the cost function into a quantum
Hamiltonian and evolving toward low-energy states.

### The mapping

1. **Decision variables:** binary -- does task i run on resource j at time slot k?
2. **Cost function:** total energy consumption (sum of power draws for all
   assignments)
3. **Constraints:** each task runs exactly once, no resource overload, deadlines met
4. **QUBO formulation:** convert constraints to penalty terms, get a single quadratic
   objective function
5. **Ising Hamiltonian:** map the QUBO to a quantum Hamiltonian
6. **QAOA circuit:** alternating cost and mixer layers, parameterized by angles
7. **Optimize:** classical optimizer tunes the angles to minimize energy

### Why this might actually work

- The problem structure is naturally binary (assign or don't assign)
- QAOA has proven approximation guarantees for certain graph problems
- The building-scale problem (10s of resources, 100s of tasks) is in the sweet
  spot for near-term quantum hardware -- too big for brute force, small enough
  for current qubit counts
- Energy minimization is smooth enough that QAOA's approximate solutions could
  be practically useful even without exact optimality

**Relevant Qiskit tools:**
- `qiskit_optimization.algorithms.QAOA` -- the solver
- `qiskit_optimization.problems.QuadraticProgram` -- problem formulation
- `qiskit_optimization.converters.QuadraticProgramToQubo` -- QUBO conversion
- `qiskit_optimization.algorithms.MinimumEigenOptimizer` -- wraps VQE/QAOA
- `qiskit.circuit.library.QAOAAnsatz` -- the circuit structure

## How this connects to the ecosystem

- **Vector** provides the building context: which resources exist, their power
  profiles, thermal status, current load. This is the "what do we have to work with"
  input.
- **Nexus** is the orchestration layer that actually dispatches tasks. Quantum Nexus
  provides the optimized schedule; Nexus executes it. This is the clearest
  integration point between the three projects.
- **The feedback loop:** Nexus reports actual energy consumption back. Over time,
  the scheduling model gets refined with real data.

### Patent boundary note

The scheduling optimization itself is generic combinatorial optimization -- well
within open research territory. What's potentially protectable is the integration
pattern: how Vector's spatial awareness feeds into the optimization constraints,
and how Nexus distributes the scheduling decisions. Keep the quantum methods clean
and generic in this repo.

## Approach for the demo

1. Define a simple building compute environment:
   - 5-10 compute resources with different power profiles
   - 20-50 tasks with varying requirements and deadlines
   - Time divided into discrete slots
2. Formulate as a QUBO problem
3. Solve classically (brute force for small instances, ILP for larger)
4. Solve with QAOA
5. Compare solution quality and compute time
6. Scale up: at what problem size does QAOA start to compete?

### The scaling question

This is the real question. For tiny problems, classical is faster (no quantum
overhead). For huge problems, we don't have enough qubits yet. The interesting
region is the middle -- where classical starts struggling but quantum hardware
can still handle it. Finding that crossover (if it exists for realistic building
scenarios) is the main research contribution.

## Open questions

- **Constraint encoding:** How to handle hard constraints (deadlines, single
  assignment) in the QUBO formulation without drowning the cost function in
  penalty terms. Too many penalties and QAOA spends all its effort satisfying
  constraints instead of optimizing energy.
- **Warm-starting QAOA:** Can we use a classical heuristic solution as the
  initial state for QAOA? Recent papers suggest this improves convergence.
- **Multi-period scheduling:** The demo starts with a single scheduling window.
  Real systems need rolling-horizon scheduling. How to decompose the time
  dimension for quantum treatment?
- **Noise tolerance:** Scheduling is a discrete problem -- small perturbations
  from hardware noise can flip assignments entirely. Need error mitigation
  or post-processing to clean up results.
- **Depth vs. quality:** More QAOA layers (higher p) generally give better
  approximations but require deeper circuits. On real hardware, deeper circuits
  mean more noise. What's the practical sweet spot?

## Key references

- Farhi, E., et al. "A quantum approximate optimization algorithm." (2014)
  -- the original QAOA paper
- Hadfield, S., et al. "From the quantum approximate optimization algorithm
  to a quantum alternating operator ansatz." (2019) -- generalized QAOA
- Egger, D., et al. "Quantum computing for finance." (2020) -- similar QUBO
  formulations for portfolio optimization (analogous problem structure)
- IBM Qiskit Optimization documentation and tutorials

## Next steps

1. Implement the compute environment model (resources, tasks, power profiles)
2. Formulate the QUBO in `qiskit_optimization.QuadraticProgram`
3. Build classical ILP baseline
4. Implement QAOA solver in a new circuit module (or extend `state_estimation.py`)
5. Run comparison in a new notebook
6. Investigate warm-starting from classical heuristics
