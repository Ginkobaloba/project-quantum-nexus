"""
02 - Quantum State Estimation Demo
====================================

This will become a Jupyter notebook demonstrating quantum-enhanced
state estimation on a simplified building power system.

Planned contents:
    1. Build a simple building power model (5-floor radial network)
    2. Generate synthetic measurements with noise
    3. Run classical WLS state estimation
    4. Formulate the cost Hamiltonian for VQE
    5. Run VQE-based state estimation on Aer simulator
    6. Compare accuracy and computational cost
    7. Explore scaling behavior

Convert to notebook with: jupyter nbconvert --to notebook 02_state_estimation_demo.py
"""

# TODO: Implement when the circuit modules are ready.

# Rough outline:
# from quantum_nexus.data.power_system_model import create_building_model, generate_measurements
# from quantum_nexus.circuits.state_estimation import (
#     classical_wls_baseline,
#     build_cost_hamiltonian,
#     run_vqe_state_estimation,
# )
# from quantum_nexus.utils.visualization import plot_state_estimation_comparison
#
# # Step 1: Build model
# model = create_building_model(num_floors=5)
#
# # Step 2: Generate measurements
# measurements, weights, H = generate_measurements(model, noise_std=0.02, seed=42)
#
# # Step 3: Classical baseline
# classical_result = classical_wls_baseline(measurements, weights, H)
#
# # Step 4-5: Quantum approach
# hamiltonian = build_cost_hamiltonian(measurements, weights, H)
# quantum_result = run_vqe_state_estimation(hamiltonian)
#
# # Step 6: Compare
# plot_state_estimation_comparison(true_state, classical_result, quantum_result)
