from typing import List, Optional, Sequence, Dict
import math
import matplotlib.pyplot as plt

# Tier definitions
TIER_BOUNDS = {
    "low":  (0, 1500),
    "mid":  (1500, 15000),  # values <15000 are mid
    "high": (15000, math.inf),
}
TIER_COLOURS = {"low": "#cce6ff", "mid": "#ccffcc", "high": "#ffe5cc"}
DEFAULT_WINDOWS = {"low": 250, "mid": 1000, "high": 1500}
INCREMENTS: List[int] = [0, 5000, 10000, 15000]
X_MIN = -500


def tier_for_value(val: float) -> str:
    if val < TIER_BOUNDS["low"][1]:
        return "low"
    if val < TIER_BOUNDS["mid"][1]:
        return "mid"
    return "high"


def plot_dual(cb_value: float,
              pb_value: float,
              payments: Optional[Sequence[float]] = None,
              window_sizes: Optional[Dict[str, float]] = None,
              x_max_limit: Optional[float] = None):
    if window_sizes is None:
        window_sizes = DEFAULT_WINDOWS

    fig, ax = plt.subplots(figsize=(13, 3))

    # Background shading
    for tier, (lo, hi) in TIER_BOUNDS.items():
        span_hi = hi if math.isfinite(hi) else (x_max_limit or lo)
        ax.axvspan(lo, span_hi, color=TIER_COLOURS[tier], alpha=0.45)

    # Draw increments & windows
    for inc in INCREMENTS:
        win = window_sizes[tier_for_value(inc)]
        ax.axvline(inc, color="black", lw=2)
        ax.text(inc, 0.32, f"${inc:,}", ha="center", va="bottom", fontsize=8)
        ax.axvspan(inc - win, inc + win, color="#d9d9d9", alpha=0.3)
        ax.axvline(inc - win, color="#666", ls="--", lw=1)
        ax.axvline(inc + win, color="#666", ls="--", lw=1)

    # Overlay payments histogram (fixed conditional)
    if payments is not None and len(payments) > 0:
        ax_hist = ax.twinx()
        ax_hist.hist(payments, bins=30, density=True, color="#444", alpha=0.25)
        ax_hist.set_yticks([])

    # Plot current and proposed benchmarks
    ax.plot(cb_value, 0.5, "o", color="red", ms=10, label="Current BM")
    ax.text(cb_value, 0.57, f"Current ${cb_value:,}", ha="center", va="bottom", color="red", fontsize=9)
    ax.plot(pb_value, 0.4, "o", color="#006400", ms=10, label="Proposed BM")
    ax.text(pb_value, 0.47, f"Proposed ${pb_value:,}", ha="center", va="bottom", color="#006400", fontsize=9)

    # X-axis limits
    auto_right = max(cb_value + 500, pb_value + 500, max(payments) if payments is not None and len(payments) > 0 else cb_value + 500)
    x_max = x_max_limit if x_max_limit is not None else auto_right
    ax.set_xlim(X_MIN, x_max)

    # Cleanup
    ax.set_ylim(0, 1)
    ax.set_xlabel("Dollar value (AUD$)")
    ax.set_yticks([])
    ax.set_title("Benchmark positions", fontsize=11, fontweight="bold")
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    return fig
