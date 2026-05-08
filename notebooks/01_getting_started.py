"""
01 - Getting Started with Quantum Nexus
========================================

This will become a Jupyter notebook. For now it's a placeholder .py file.

Planned contents:
    - Install and import verification
    - Quick tour of the package structure
    - Generate some simulated sensor data
    - Build a simple quantum circuit
    - Run it on the Aer simulator
    - Verify that Qiskit and all dependencies are working

Convert to notebook with: jupyter nbconvert --to notebook 01_getting_started.py
"""

# TODO: Convert this to a proper .ipynb once the dependencies are installed.

# Quick smoke test -- uncomment when deps are available:
# from quantum_nexus.data.simulated_sensors import generate_normal_data, BuildingConfig
# config = BuildingConfig(num_zones=3)
# data = generate_normal_data(config, num_timesteps=10, seed=42)
# print(data.head())
# print(f"Generated {len(data)} timesteps across {config.num_zones} zones")
