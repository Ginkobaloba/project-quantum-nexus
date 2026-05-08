# Quantum Kernel Methods for Distributed Anomaly Detection

**Status:** Research notes. Updated 2026-05-08.

---

## The problem

Distributed sensor networks generate massive streams of multivariate time-series
data. Hidden in that stream: equipment failures, cybersecurity intrusions, sensor
degradation, environmental anomalies. Classical anomaly detection works, but it
struggles with:

- High-dimensional feature spaces (dozens of correlated sensor channels)
- Non-linear decision boundaries between normal and anomalous behavior
- Concept drift as building conditions change over time
- The "needle in a haystack" ratio -- anomalies are rare by definition

## Why quantum kernels?

Kernel methods (SVM, kernel PCA, etc.) map data into high-dimensional feature
spaces where linear separation becomes possible. The kernel function defines the
geometry of that mapping.

Quantum kernels use parameterized quantum circuits to compute the kernel function.
The claim: quantum circuits can access feature spaces that are exponentially hard
for classical computers to compute, potentially finding decision boundaries that
classical kernels miss.

### The quantum kernel trick

1. Encode data point x into a quantum state |phi(x)>
2. Encode data point y into |phi(y)>
3. The kernel value K(x,y) = |<phi(x)|phi(y)>|^2
4. This inner product is computed by the quantum hardware
5. The resulting kernel matrix feeds into a classical SVM

The quantum part is "just" computing the kernel. Everything else (SVM training,
prediction, etc.) stays classical. This is a nice property -- you get quantum
enhancement without needing a fully quantum pipeline.

### Quantum feature maps

The encoding circuit determines what feature space we're working in. Options:

- **ZZFeatureMap** -- encodes pairwise correlations between features. Good for data
  where interactions between sensor channels matter (spoiler: they do).
- **PauliFeatureMap** -- more flexible, allows custom Pauli rotation gates. Can
  encode higher-order correlations.
- **Custom circuits** -- problem-specific encodings tailored to the sensor data
  structure.

**Relevant Qiskit tools:**
- `qiskit.circuit.library.ZZFeatureMap`
- `qiskit.circuit.library.PauliFeatureMap`
- `qiskit_machine_learning.kernels.FidelityQuantumKernel`
- `qiskit_machine_learning.algorithms.QSVC` -- quantum SVM classifier

## How this connects to the ecosystem

- **Vector** generates the sensor data that needs anomaly monitoring. In the real
  system, Vector's edge processors do first-pass anomaly detection locally.
  Quantum-enhanced methods would handle the harder cases -- subtle multi-sensor
  correlations that simple threshold checks miss.
- **Nexus** distributes the anomaly detection workload. Different Nexus nodes
  could handle different building zones or sensor clusters.

The quantum anomaly classifier here is a research tool. If it proves effective,
the method (not the Vector-specific implementation) could be published as an open
contribution to quantum ML literature.

## Approach for the demo

1. Generate synthetic sensor data with injected anomalies:
   - Gradual sensor drift (simulates calibration failure)
   - Sudden spikes (simulates equipment failure)
   - Correlated multi-sensor anomalies (simulates HVAC system failures)
   - Subtle pattern shifts (the hard ones -- simulates occupancy changes or
     cybersecurity probing)
2. Build a classical SVM baseline with RBF kernel
3. Build quantum kernel SVM using ZZFeatureMap
4. Compare classification accuracy, especially on the subtle patterns
5. Analyze which anomaly types benefit from quantum kernels

## Open questions

- **Feature selection:** Quantum circuits have limited qubits. Which sensor
  features encode into the quantum kernel? PCA first, or let the circuit handle
  dimensionality?
- **Training data size:** Quantum kernel computation is O(n^2) in training samples
  (same as classical kernels). For large datasets, we need subsampling or
  approximation. How does this affect anomaly detection performance?
- **Noise impact:** Quantum hardware noise could actually help or hurt anomaly
  detection. Noise might regularize the classifier (like dropout in neural nets)
  or it might wash out the subtle patterns we're trying to detect.
- **Real-time feasibility:** Can we compute quantum kernels fast enough for
  real-time anomaly detection? Current queue times on IBM hardware say no, but
  that's a hardware access issue, not an algorithmic one.

## Key references

- Havlicek, V., et al. "Supervised learning with quantum-enhanced feature spaces."
  Nature 567 (2019)
- Schuld, M., "Quantum machine learning models are kernel methods." (2021)
- Liu, Y., et al. "A rigorous and robust quantum speed-up in supervised ML." (2021)
- Qiskit Machine Learning documentation

## Next steps

1. Implement synthetic anomaly injection in `simulated_sensors.py`
2. Build classical SVM baseline
3. Implement quantum kernel classifier in `anomaly_classifier.py`
4. Run comparison in `03_anomaly_detection_demo` notebook
5. If results look promising, explore custom feature maps tailored to sensor data
