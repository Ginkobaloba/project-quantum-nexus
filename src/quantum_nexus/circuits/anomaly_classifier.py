"""
Quantum circuits for power system anomaly detection.

Two approaches implemented (well, stubbed):
1. Quantum kernel method -- compute kernel matrix in quantum feature space,
   feed to classical one-class SVM
2. Variational quantum classifier -- train a parameterized circuit directly
   as a binary classifier (normal vs. anomaly)

Both approaches are probably overkill for the data sizes we're working with.
But "probably overkill" is the unofficial motto of quantum computing research.
"""

from typing import Optional

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes


class AnomalyClassifierCircuit:
    """Quantum circuits for anomaly detection in sensor data.

    Supports two modes:
    - "kernel": quantum kernel computation for use with classical SVM
    - "variational": end-to-end parameterized quantum classifier

    Attributes:
        num_features: Number of input features (sensor channels).
        num_qubits: Number of qubits (equals num_features for angle encoding).
        mode: "kernel" or "variational".
    """

    def __init__(
        self,
        num_features: int,
        mode: str = "kernel",
        feature_map_reps: int = 2,
        variational_reps: int = 3,
    ) -> None:
        """Initialize the anomaly classifier circuit.

        Args:
            num_features: Number of sensor features to encode.
            mode: Classification mode -- "kernel" or "variational".
            feature_map_reps: Repetitions in the feature map circuit.
            variational_reps: Repetitions in the variational ansatz (variational mode only).
        """
        self.num_features = num_features
        self.num_qubits = num_features  # angle encoding: one qubit per feature
        self.mode = mode
        self.feature_map_reps = feature_map_reps
        self.variational_reps = variational_reps

    def build_feature_map(self) -> QuantumCircuit:
        """Build the feature map circuit for data encoding.

        Uses ZZFeatureMap which encodes features via single-qubit rotations
        and captures pairwise correlations via ZZ entangling gates. This is
        a reasonable default for sensor data where pairwise correlations
        between channels carry information.

        Returns:
            Parameterized QuantumCircuit for feature encoding.

        TODO: Explore custom feature maps that encode known physics.
              For power systems, voltage-current relationships follow
              specific patterns that a physics-informed feature map
              could exploit. ZZFeatureMap is generic -- we can do better.
        """
        return ZZFeatureMap(
            feature_dimension=self.num_features,
            reps=self.feature_map_reps,
            entanglement="linear",  # TODO: try "circular" for periodic sensor layouts
        )

    def build_kernel_circuit(
        self,
        x1: np.ndarray,
        x2: np.ndarray,
    ) -> QuantumCircuit:
        """Build circuit to compute quantum kernel entry k(x1, x2).

        The kernel value is the fidelity between the quantum states
        produced by encoding x1 and x2 through the feature map:
        k(x1, x2) = |<phi(x1)|phi(x2)>|^2

        Args:
            x1: First data point (feature vector).
            x2: Second data point (feature vector).

        Returns:
            QuantumCircuit that, when measured, yields the kernel value.

        TODO: Implement the fidelity circuit:
              1. Apply feature map with x1
              2. Apply inverse feature map with x2
              3. Measure -- probability of all-zeros state gives kernel value
        """
        if len(x1) != self.num_features or len(x2) != self.num_features:
            raise ValueError(
                f"Feature vectors must have length {self.num_features}, "
                f"got {len(x1)} and {len(x2)}."
            )

        # Placeholder -- returns empty circuit
        # Real implementation: feature_map(x1) + feature_map_inverse(x2)
        qc = QuantumCircuit(self.num_qubits)
        # TODO: encode x1, apply inverse encoding of x2, measure
        return qc

    def build_variational_classifier(self) -> QuantumCircuit:
        """Build the full variational quantum classifier circuit.

        Architecture: feature_map -> variational_ansatz -> measurement

        Returns:
            Parameterized QuantumCircuit for training as a classifier.

        TODO: Implement the combined circuit:
              1. Feature map layer (data encoding)
              2. Variational ansatz (trainable parameters)
              3. Define measurement scheme (which qubits map to class labels)
        """
        feature_map = self.build_feature_map()
        ansatz = RealAmplitudes(
            num_qubits=self.num_qubits,
            reps=self.variational_reps,
            entanglement="linear",
        )

        # Compose feature map + ansatz
        # TODO: actually compose these circuits and add measurement
        qc = QuantumCircuit(self.num_qubits)
        return qc

    def compute_kernel_matrix(
        self,
        X_train: np.ndarray,
        X_test: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Compute the quantum kernel matrix.

        Args:
            X_train: Training data matrix (n_samples x n_features).
            X_test: Optional test data. If None, computes train-train kernel.

        Returns:
            Kernel matrix as numpy array.

        TODO: Implement kernel computation:
              1. For each pair (x_i, x_j), build and run fidelity circuit
              2. Collect measurement statistics
              3. Estimate kernel values from all-zeros probabilities
              4. Assemble into kernel matrix
              This is O(n^2) circuit executions. On real hardware,
              use batching and caching aggressively.
        """
        n_train = X_train.shape[0]
        n_test = X_test.shape[0] if X_test is not None else n_train

        # Placeholder -- identity-ish matrix
        # The universe is a simulation anyway, so a simulated kernel is fine
        return np.eye(n_train, n_test)

    def classify(
        self,
        X: np.ndarray,
        threshold: float = 0.5,
    ) -> np.ndarray:
        """Classify data points as normal (0) or anomalous (1).

        Args:
            X: Data matrix (n_samples x n_features).
            threshold: Classification threshold.

        Returns:
            Binary array of predictions.

        TODO: Implement classification pipeline:
              - Kernel mode: compute kernel matrix, run one-class SVM
              - Variational mode: run trained circuit, interpret measurements
        """
        # Placeholder -- everything is normal, nothing to see here
        return np.zeros(X.shape[0], dtype=int)
