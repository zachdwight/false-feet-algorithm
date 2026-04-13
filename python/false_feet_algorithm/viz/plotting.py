"""
Visualization utilities for the False Feet Algorithm.

Provides plotting functions for understanding algorithm behavior and results.
Matplotlib is optional - these functions gracefully degrade if not available.
"""

from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    logger.debug("Matplotlib not available. Visualization functions will be disabled.")


def _require_matplotlib(func_name: str) -> None:
    """Raise helpful error if matplotlib is not available."""
    if not HAS_MATPLOTLIB:
        raise ImportError(
            f"'{func_name}' requires matplotlib. "
            "Install with: pip install false-feet-algorithm[viz]"
        )


class AlgorithmVisualizer:
    """Utilities for visualizing Amoeba algorithm behavior."""

    def __init__(self, solver: "AmoebaInvestigation"):
        """
        Initialize visualizer with a solver instance.

        Args:
            solver: AmoebaInvestigation instance to visualize
        """
        self.solver = solver
        self.iteration_data: List[Dict] = []

    def track_iteration(self, iteration: int, alive_count: int, best_score: float) -> None:
        """
        Record data for an iteration (call from solver if tracking).

        Args:
            iteration: Iteration number
            alive_count: Number of alive branches
            best_score: Highest branch score
        """
        self.iteration_data.append({
            "iteration": iteration,
            "alive_count": alive_count,
            "best_score": best_score,
        })

    def plot_option_scores(
        self,
        title: str = "Final Hypothesis Scores",
        figsize: Tuple[int, int] = (10, 6)
    ) -> None:
        """
        Plot final scores for all options.

        Args:
            title: Plot title
            figsize: Figure size (width, height)
        """
        _require_matplotlib("plot_option_scores")

        branches = self.solver.get_branches()
        if not branches:
            logger.warning("No branches to plot")
            return

        option_names = [b.option.name for b in branches]
        scores = [b.get_score() for b in branches]
        colors = ["green" if b.is_alive() else "lightgray" for b in branches]

        fig, ax = plt.subplots(figsize=figsize)
        bars = ax.bar(option_names, scores, color=colors, edgecolor="black", linewidth=2)

        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.02,
                f"{score:.3f}",
                ha="center",
                va="bottom",
                fontweight="bold"
            )

        ax.set_ylim(0, 1.1)
        ax.set_ylabel("Score (0.0 - 1.0)", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        # Legend
        alive_patch = mpatches.Patch(color="green", label="Alive")
        dead_patch = mpatches.Patch(color="lightgray", label="Culled")
        ax.legend(handles=[alive_patch, dead_patch], loc="upper right")

        plt.tight_layout()
        return fig

    def plot_branch_survival(
        self,
        title: str = "Branch Survival Over Iterations",
        figsize: Tuple[int, int] = (12, 6)
    ) -> None:
        """
        Plot which branches survive each iteration.

        Args:
            title: Plot title
            figsize: Figure size (width, height)
        """
        _require_matplotlib("plot_branch_survival")

        # Get iteration data from solver's history
        # Note: This requires the solver to track history (optional enhancement)
        if not hasattr(self.solver, "_iteration_history"):
            logger.warning("Solver did not track iteration history. Enable with solver.track_history=True")
            return

        history = self.solver._iteration_history
        iterations = [h["iteration"] for h in history]
        alive_counts = [h["alive_branches"] for h in history]

        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(iterations, alive_counts, marker="o", linewidth=2, markersize=6, color="darkblue")
        ax.fill_between(iterations, alive_counts, alpha=0.3, color="lightblue")

        ax.set_xlabel("Iteration", fontsize=12)
        ax.set_ylabel("Number of Alive Branches", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, len(self.solver.branches) + 0.5)

        plt.tight_layout()
        return fig

    def plot_convergence_progress(
        self,
        title: str = "Convergence Progress",
        figsize: Tuple[int, int] = (12, 6)
    ) -> None:
        """
        Plot best score progression over iterations.

        Args:
            title: Plot title
            figsize: Figure size (width, height)
        """
        _require_matplotlib("plot_convergence_progress")

        if not hasattr(self.solver, "_iteration_history"):
            logger.warning("Solver did not track iteration history")
            return

        history = self.solver._iteration_history
        iterations = [h["iteration"] for h in history]
        best_scores = [h["best_score"] for h in history]

        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(iterations, best_scores, marker="o", linewidth=2.5, markersize=7, color="darkgreen")
        ax.fill_between(iterations, best_scores, alpha=0.3, color="lightgreen")

        ax.axhline(y=1.0, color="red", linestyle="--", linewidth=2, alpha=0.7, label="Perfect Score")
        ax.set_xlabel("Iteration", fontsize=12)
        ax.set_ylabel("Best Score", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim(0, 1.1)

        plt.tight_layout()
        return fig

    @staticmethod
    def show_all():
        """Display all active plots (call after creating plots)."""
        if not HAS_MATPLOTLIB:
            logger.warning("Matplotlib not available")
            return
        plt.show()

    @staticmethod
    def save_figure(filename: str) -> None:
        """
        Save the current figure to file.

        Args:
            filename: Output filename (e.g., 'plot.png', 'plot.pdf')
        """
        if not HAS_MATPLOTLIB:
            logger.warning("Matplotlib not available")
            return
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        logger.info(f"Saved plot to {filename}")


def plot_problem_space(
    problem: "Problem",
    figsize: Tuple[int, int] = (12, 8)
) -> None:
    """
    Visualize the problem space (options and evidence).

    Shows a network graph of options and supporting/contradicting evidence.

    Args:
        problem: Problem instance to visualize
        figsize: Figure size (width, height)
    """
    _require_matplotlib("plot_problem_space")

    try:
        import networkx as nx
    except ImportError:
        logger.warning("NetworkX required for plot_problem_space. Install with: pip install networkx")
        return

    # Create graph
    G = nx.DiGraph()

    # Add nodes for options
    for option in problem.options:
        G.add_node(option.id, label=option.name, node_type="option")

    # Add nodes for data points
    for data in problem.data_points:
        G.add_node(data.id, label=data.title, node_type="data")

    # Add edges
    for data in problem.data_points:
        for opt_id in data.supports:
            G.add_edge(data.id, opt_id, edge_type="supports")
        for opt_id in data.contradicts:
            G.add_edge(data.id, opt_id, edge_type="contradicts")

    # Layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Draw
    fig, ax = plt.subplots(figsize=figsize)

    # Draw nodes
    option_nodes = [n for n, attr in G.nodes(data=True) if attr.get("node_type") == "option"]
    data_nodes = [n for n, attr in G.nodes(data=True) if attr.get("node_type") == "data"]

    nx.draw_networkx_nodes(G, pos, nodelist=option_nodes, node_color="lightblue",
                          node_size=2000, ax=ax, label="Options")
    nx.draw_networkx_nodes(G, pos, nodelist=data_nodes, node_color="lightyellow",
                          node_size=1500, ax=ax, label="Evidence")

    # Draw edges
    support_edges = [e for e, attr in G.edges(data=True) if attr.get("edge_type") == "supports"]
    contradict_edges = [e for e, attr in G.edges(data=True) if attr.get("edge_type") == "contradicts"]

    nx.draw_networkx_edges(G, pos, edgelist=support_edges, edge_color="green",
                          width=2, alpha=0.6, ax=ax, arrowsize=15, label="Supports")
    nx.draw_networkx_edges(G, pos, edgelist=contradict_edges, edge_color="red",
                          width=2, alpha=0.6, ax=ax, arrowsize=15, style="dashed", label="Contradicts")

    # Draw labels
    labels = {n: attr.get("label", n) for n, attr in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="bold", ax=ax)

    ax.set_title(problem.title, fontsize=14, fontweight="bold")
    ax.legend(loc="upper left", fontsize=10)
    ax.axis("off")

    plt.tight_layout()
    return fig
