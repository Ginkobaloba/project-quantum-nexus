"""
03 - Quantum Anomaly Detection Demo
=====================================

This will become a Jupyter notebook demonstrating quantum kernel methods
for anomaly detection in building sensor data.

Planned contents:
    1. Generate normal building sensor data
    2. Inject different types of anomalies
    3. Train classical SVM with RBF kernel
    4. Train quantum kernel SVM with ZZFeatureMap
    5. Compare detection accuracy across anomaly types
    6. Analyze which anomaly types benefit from quantum kernels
    7. Visualize decision boundaries (2D projection)

Convert to notebook with: jupyter nbconvert --to notebook 03_anomaly_detection_demo.py
"""

# TODO: Implement when the classifier modules are ready.

# Rough outline:
# from quantum_nexus.data.simulated_sensors import (
#     generate_normal_data,
#     inject_anomalies,
#     BuildingConfig,
# )
# from quantum_nexus.circuits.anomaly_classifier import (
#     train_quantum_svm,
#     classical_svm_baseline,
# )
# from quantum_nexus.utils.visualization import plot_anomaly_detection_results
#
# # Generate data
# config = BuildingConfig(num_zones=3)
# normal_data = generate_normal_data(config, num_timesteps=500, seed=42)
# data, labels = inject_anomalies(normal_data, anomaly_type="correlated", fraction=0.05)
#
# # Classical baseline
# classical_clf = classical_svm_baseline(features, labels)
#
# # Quantum kernel
# quantum_clf = train_quantum_svm(features, labels)
#
# # Compare
# plot_anomaly_detection_results(features, labels, quantum_predictions)
