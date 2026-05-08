"""
Simulated sensor data generation for power system testing.

Generates synthetic sensor readings that approximate the statistical properties
of real building management system sensors: voltage, current, power factor,
temperature, humidity, and occupancy.

None of this data is real. But it's real enough to test quantum circuits against,
which is the whole point. If you want real data, go install some sensors.
"""

from typing import Optional

import numpy as np
import pandas as pd


class SensorSimulator:
    """Generate simulated sensor data for power system testing.

    Creates time-series data for multiple sensor channels with configurable
    noise levels, correlation structures, and anomaly injection.

    Attributes:
        num_sensors: Number of sensor channels.
        sample_rate_hz: Sampling frequency in Hz.
        noise_std: Standard deviation of Gaussian measurement noise.
        seed: Random seed for reproducibility.
    """

    def __init__(
        self,
        num_sensors: int = 10,
        sample_rate_hz: float = 1.0,
        noise_std: float = 0.05,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize the sensor simulator.

        Args:
            num_sensors: Number of sensor channels to simulate.
            sample_rate_hz: Sampling rate in Hz.
            noise_std: Measurement noise standard deviation (relative to signal).
            seed: Random seed. Set for reproducible results.
        """
        self.num_sensors = num_sensors
        self.sample_rate_hz = sample_rate_hz
        self.noise_std = noise_std
        self.rng = np.random.default_rng(seed)

    def generate_normal_data(
        self,
        duration_seconds: int = 3600,
        include_diurnal: bool = True,
    ) -> pd.DataFrame:
        """Generate normal (non-anomalous) sensor data.

        Creates baseline sensor readings with realistic temporal patterns
        and inter-sensor correlations.

        Args:
            duration_seconds: Length of time series in seconds.
            include_diurnal: Add diurnal (24h) variation pattern.

        Returns:
            DataFrame with columns for each sensor and a datetime index.

        TODO: Implement realistic sensor data generation:
              1. Base signals with configurable mean/variance per channel
              2. Diurnal patterns (temperature follows sun, power follows occupancy)
              3. Inter-sensor correlations (voltage and current, temp and HVAC)
              4. Gaussian noise overlay
              5. Occasional missing values (realistic sensor behavior)
        """
        num_samples = int(duration_seconds * self.sample_rate_hz)
        timestamps = pd.date_range(
            start="2026-01-01",
            periods=num_samples,
            freq=f"{1/self.sample_rate_hz}s",
        )

        # Placeholder -- uniform random data
        # Real implementation should have physics-informed base signals
        data = self.rng.standard_normal((num_samples, self.num_sensors))
        columns = [f"sensor_{i:03d}" for i in range(self.num_sensors)]

        return pd.DataFrame(data, index=timestamps, columns=columns)

    def inject_anomaly(
        self,
        data: pd.DataFrame,
        anomaly_type: str = "spike",
        start_idx: Optional[int] = None,
        duration_samples: int = 10,
        magnitude: float = 5.0,
        affected_sensors: Optional[list[int]] = None,
    ) -> tuple[pd.DataFrame, np.ndarray]:
        """Inject synthetic anomalies into sensor data.

        Args:
            data: Normal sensor data DataFrame.
            anomaly_type: Type of anomaly. One of "spike", "drift", "dropout", "correlation_break".
            start_idx: Start index for anomaly. Random if None.
            duration_samples: Number of samples the anomaly persists.
            magnitude: Anomaly magnitude (interpretation depends on type).
            affected_sensors: Which sensor indices are affected. Random subset if None.

        Returns:
            Tuple of (modified DataFrame, binary labels array where 1 = anomalous).

        TODO: Implement anomaly injection:
              - "spike": sudden magnitude change (sensor fault, power surge)
              - "drift": gradual shift in baseline (calibration drift, degradation)
              - "dropout": missing/zero values (communication failure)
              - "correlation_break": change in inter-sensor correlation (physical change)
        """
        modified = data.copy()
        labels = np.zeros(len(data), dtype=int)

        if start_idx is None:
            start_idx = self.rng.integers(0, len(data) - duration_samples)

        # Mark anomalous region
        labels[start_idx : start_idx + duration_samples] = 1

        # TODO: actually inject the anomaly based on type
        # For now, just mark the labels. The quantum classifier needs to
        # detect something that isn't there yet. Very zen.

        return modified, labels

    def get_feature_names(self) -> list[str]:
        """Return the sensor channel names.

        Returns:
            List of sensor name strings.
        """
        return [f"sensor_{i:03d}" for i in range(self.num_sensors)]
