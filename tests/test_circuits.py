"""
Tests for quantum circuit modules.

These tests verify that circuit construction and basic operations work
correctly. They do NOT test for quantum advantage -- that's a research
question, not a unit test. (Though if someone figures out how to
unit test for quantum advantage, publish that immediately.)
"""

import numpy as np
import pytest

from quantum_nexus.circuits.state_estimation import StateEstimationCircuit
from quantum_nexus.circuits.anomaly_classifier import AnomalyClassifierCircuit


class TestStateEstimationCircuit:
    """Tests for the VQE state estimation circuit."""

    def test_init_default(self) -> None:
        """Test default initialization."""
        circuit = StateEstimationCircuit(num_buses=4)
        assert circuit.num_buses == 4
        assert circuit.num_qubits == 4
        assert circuit.ansatz_type == "efficient_su2"
        assert circuit.reps == 2

    def test_init_custom(self) -> None:
        """Test custom initialization."""
        circuit = StateEstimationCircuit(
            num_buses=8,
            ansatz_type="real_amplitudes",
            reps=3,
        )
        assert circuit.num_buses == 8
        assert circuit.ansatz_type == "real_amplitudes"
        assert circuit.reps == 3

    def test_build_ansatz_efficient_su2(self) -> None:
        """Test EfficientSU2 ansatz construction."""
        circuit = StateEstimationCircuit(num_buses=4, ansatz_type="efficient_su2")
        ansatz = circuit.build_ansatz()
        assert ansatz.num_qubits == 4

    def test_build_ansatz_real_amplitudes(self) -> None:
        """Test RealAmplitudes ansatz construction."""
        circuit = StateEstimationCircuit(num_buses=4, ansatz_type="real_amplitudes")
        ansatz = circuit.build_ansatz()
        assert ansatz.num_qubits == 4

    def test_build_ansatz_invalid_type(self) -> None:
        """Test that invalid ansatz type raises ValueError."""
        circuit = StateEstimationCircuit(num_buses=4, ansatz_type="nonexistent")
        with pytest.raises(ValueError, match="Unknown ansatz type"):
            circuit.build_ansatz()

    def test_build_cost_hamiltonian_returns_dict(self) -> None:
        """Test that cost Hamiltonian returns a dictionary."""
        circuit = StateEstimationCircuit(num_buses=4)
        measurements = np.array([1.0, 0.95, 1.02, 0.98])
        result = circuit.build_cost_hamiltonian(measurements)
        assert isinstance(result, dict)

    def test_run_estimation_returns_expected_keys(self) -> None:
        """Test that run_estimation returns all expected keys."""
        circuit = StateEstimationCircuit(num_buses=4)
        measurements = np.array([1.0, 0.95, 1.02, 0.98])
        result = circuit.run_estimation(measurements)
        expected_keys = {
            "estimated_state",
            "cost",
            "convergence",
            "optimal_params",
            "num_iterations",
        }
        assert set(result.keys()) == expected_keys


class TestAnomalyClassifierCircuit:
    """Tests for the quantum anomaly classifier."""

    def test_init_default(self) -> None:
        """Test default initialization."""
        classifier = AnomalyClassifierCircuit(num_features=4)
        assert classifier.num_features == 4
        assert classifier.num_qubits == 4
        assert classifier.mode == "kernel"

    def test_build_feature_map(self) -> None:
        """Test feature map construction."""
        classifier = AnomalyClassifierCircuit(num_features=4)
        feature_map = classifier.build_feature_map()
        assert feature_map.num_qubits == 4

    def test_build_kernel_circuit_dimension_check(self) -> None:
        """Test that kernel circuit rejects wrong-size inputs."""
        classifier = AnomalyClassifierCircuit(num_features=4)
        x1 = np.array([1.0, 2.0, 3.0])  # wrong size
        x2 = np.array([1.0, 2.0, 3.0, 4.0])
        with pytest.raises(ValueError, match="must have length"):
            classifier.build_kernel_circuit(x1, x2)

    def test_compute_kernel_matrix_shape(self) -> None:
        """Test kernel matrix has correct shape."""
        classifier = AnomalyClassifierCircuit(num_features=4)
        X = np.random.randn(10, 4)
        K = classifier.compute_kernel_matrix(X)
        assert K.shape == (10, 10)

    def test_classify_returns_binary(self) -> None:
        """Test that classify returns binary predictions."""
        classifier = AnomalyClassifierCircuit(num_features=4)
        X = np.random.randn(20, 4)
        predictions = classifier.classify(X)
        assert predictions.shape == (20,)
        assert set(np.unique(predictions)).issubset({0, 1})
