"""
Tests for data generation modules.

Verifying that fake data looks fake in the right way.
"""

import numpy as np
import pandas as pd
import pytest

from quantum_nexus.data.simulated_sensors import SensorSimulator
from quantum_nexus.data.power_system_model import PowerSystemModel


class TestSensorSimulator:
    """Tests for the sensor data simulator."""

    def test_init_default(self) -> None:
        """Test default initialization."""
        sim = SensorSimulator()
        assert sim.num_sensors == 10
        assert sim.sample_rate_hz == 1.0

    def test_generate_normal_data_shape(self) -> None:
        """Test that generated data has correct shape."""
        sim = SensorSimulator(num_sensors=5, sample_rate_hz=1.0, seed=42)
        data = sim.generate_normal_data(duration_seconds=60)
        assert isinstance(data, pd.DataFrame)
        assert data.shape == (60, 5)

    def test_generate_normal_data_columns(self) -> None:
        """Test that columns are properly named."""
        sim = SensorSimulator(num_sensors=3, seed=42)
        data = sim.generate_normal_data(duration_seconds=10)
        assert list(data.columns) == ["sensor_000", "sensor_001", "sensor_002"]

    def test_reproducibility_with_seed(self) -> None:
        """Test that same seed produces same data."""
        sim1 = SensorSimulator(num_sensors=3, seed=42)
        sim2 = SensorSimulator(num_sensors=3, seed=42)
        data1 = sim1.generate_normal_data(duration_seconds=10)
        data2 = sim2.generate_normal_data(duration_seconds=10)
        pd.testing.assert_frame_equal(data1, data2)

    def test_inject_anomaly_returns_labels(self) -> None:
        """Test that anomaly injection returns data and labels."""
        sim = SensorSimulator(num_sensors=5, seed=42)
        data = sim.generate_normal_data(duration_seconds=60)
        modified, labels = sim.inject_anomaly(data, duration_samples=10)
        assert isinstance(modified, pd.DataFrame)
        assert labels.shape == (60,)
        assert labels.sum() == 10  # 10 anomalous samples

    def test_get_feature_names(self) -> None:
        """Test feature name generation."""
        sim = SensorSimulator(num_sensors=3)
        names = sim.get_feature_names()
        assert len(names) == 3
        assert names[0] == "sensor_000"


class TestPowerSystemModel:
    """Tests for the power system model."""

    def test_init_4bus(self) -> None:
        """Test 4-bus system initialization."""
        model = PowerSystemModel(system_type="ieee_4bus")
        assert model.num_buses == 4
        assert model.system_type == "ieee_4bus"

    def test_init_invalid_system(self) -> None:
        """Test that invalid system type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown system type"):
            PowerSystemModel(system_type="ieee_9000bus")

    def test_admittance_matrix_shape(self) -> None:
        """Test Y-bus matrix dimensions."""
        model = PowerSystemModel(system_type="ieee_4bus")
        Y = model.get_admittance_matrix()
        assert Y.shape == (4, 4)
        assert Y.dtype == complex

    def test_generate_measurements_keys(self) -> None:
        """Test that measurement generation returns expected keys."""
        model = PowerSystemModel(system_type="ieee_4bus")
        result = model.generate_measurements(seed=42)
        expected_keys = {"measurements", "true_state", "measurement_types", "noise_covariance"}
        assert set(result.keys()) == expected_keys

    def test_generate_measurements_dimensions(self) -> None:
        """Test measurement dimensions match system size."""
        model = PowerSystemModel(system_type="ieee_4bus")
        result = model.generate_measurements(redundancy_ratio=2.0, seed=42)
        state_size = 2 * model.num_buses  # V and theta per bus
        expected_measurements = int(state_size * 2.0)
        assert len(result["measurements"]) == expected_measurements

    def test_solve_power_flow_returns_dict(self) -> None:
        """Test that power flow solver returns expected structure."""
        model = PowerSystemModel(system_type="ieee_4bus")
        result = model.solve_power_flow()
        assert "converged" in result
        assert "state" in result
        assert "iterations" in result
