"""
Visualization utilities for quantum circuit results and analysis.

Matplotlib-based plotting for circuit outputs, convergence tracking,
and state comparison. Nothing revolutionary here -- just the plots
you'll want after every experiment to convince yourself the optimizer
didn't just wander off into a corner of parameter space and die.
"""

from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_circuit_results(
    counts: dict[str, int],
    title: str = "Circuit Measurement Results",
    figsize: tuple[int, int] = (10, 6),
) -> Figure:
    """Plot measurement results as a histogram.

    Args:
        counts: Measurement outcome counts (bitstring -> count).
        title: Plot title.
        figsize: Figure dimensions.

    Returns:
        Matplotlib Figure object.

    TODO: Implement histogram plot:
          - Sort bitstrings by count (descending)
          - Truncate to top 20 if too many outcomes
          - Color-code by expected vs. unexpected outcomes
          - Add probability annotations
    """
    fig, ax = plt.subplots(figsize=figsize)
    if counts:
        labels = list(counts.keys())
        values = list(counts.values())
        ax.bar(labels, values)
        ax.set_xlabel("Measurement Outcome")
        ax.set_ylabel("Counts")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_convergence(
    cost_history: list[float],
    title: str = "VQE Convergence",
    target_cost: Optional[float] = None,
    figsize: tuple[int, int] = (10, 6),
) -> Figure:
    """Plot optimizer convergence history.

    Args:
        cost_history: List of cost function values per iteration.
        title: Plot title.
        target_cost: Optional known optimal cost for reference line.
        figsize: Figure dimensions.

    Returns:
        Matplotlib Figure object.

    TODO: Add features:
          - Running average line for noisy optimizers
          - Confidence bands from repeated runs
          - Mark the iteration where convergence was "good enough"
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(cost_history, "b-", linewidth=1.5, label="Cost")

    if target_cost is not None:
        ax.axhline(
            y=target_cost,
            color="r",
            linestyle="--",
            label=f"Target: {target_cost:.4f}",
        )
        ax.legend()

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Cost Function Value")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_state_comparison(
    true_state: np.ndarray,
    estimated_state: np.ndarray,
    labels: Optional[list[str]] = None,
    title: str = "State Estimation Comparison",
    figsize: tuple[int, int] = (12, 6),
) -> Figure:
    """Plot true vs. estimated state variables side by side.

    Args:
        true_state: Known true state vector.
        estimated_state: Estimated state vector.
        labels: Optional labels for each state variable.
        title: Plot title.
        figsize: Figure dimensions.

    Returns:
        Matplotlib Figure object.

    TODO: Add error bars, residual subplot, and per-variable error metrics.
    """
    n = len(true_state)
    if labels is None:
        labels = [f"x_{i}" for i in range(n)]

    x_pos = np.arange(n)
    width = 0.35

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(x_pos - width / 2, true_state, width, label="True", color="steelblue")
    ax.bar(x_pos + width / 2, estimated_state, width, label="Estimated", color="coral")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("Value")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig
