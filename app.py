import streamlit as st
import numpy as np
from at_visuals import plot_dual, tier_for_value, INCREMENTS

st.set_page_config(page_title="AT Benchmark Explorer", layout="wide")
st.title("🔍 Assistive-Technology Benchmark Explorer – Single View")

# Sidebar controls
with st.sidebar:
    st.header("Benchmarks & Settings")
    current_bm = st.number_input("Current Benchmark (AUD$)", 0.0, 100000.0, 10700.0, 100.0)
    proposed_bm = st.slider("Proposed Benchmark (AUD$)", 0, 100000, int(current_bm), 100)

    st.subheader("Window half-widths (±)")
    win_low  = st.number_input("Low-cost window",  0.0, 10000.0,  250.0, 50.0)
    win_mid  = st.number_input("Mid-cost window",  0.0, 10000.0, 1000.0, 50.0)
    win_high = st.number_input("High-cost window", 0.0, 10000.0, 1500.0, 50.0)
    window_dict = {"low": win_low, "mid": win_mid, "high": win_high}

    st.subheader("Plot X-axis limit")
    x_axis_max = st.number_input("X-axis upper limit (AUD$)", 0.0, 100000.0, 20000.0, 100.0)

    st.markdown("---")
    st.subheader("Payment Distribution Stats")
    c1, c2 = st.columns(2)
    with c1:
        n      = st.number_input("N payments", min_value=10, value=1000)
        mean   = st.number_input("Mean",  min_value=0.0, value=9800.0, step=100.0)
        std    = st.number_input("Std Dev", min_value=0.0, value=4200.0, step=100.0)
        pmin   = st.number_input("Min",  min_value=0.0, value=50.0, step=50.0)
        pmax   = st.number_input("Max",  min_value=0.0, value=24000.0, step=100.0)
        skew   = st.number_input("Skewness", value=0.8)
        kurt   = st.number_input("Kurtosis", value=3.1)
    with c2:
        median = st.number_input("Median", min_value=0.0, value=9600.0, step=100.0)
        p25    = st.number_input("25th percentile", min_value=0.0, value=6000.0, step=100.0)
        p75    = st.number_input("75th percentile", min_value=0.0, value=13000.0, step=100.0)
        p90    = st.number_input("90th percentile", min_value=0.0, value=18000.0, step=100.0)
        low_b  = st.number_input("N ≤ 10 % of CB", min_value=0, value=30)
        high_b = st.number_input("N ≥ 180 % of CB", min_value=0, value=45)

# Simulate payments via selectable distribution
    dist_choice = st.selectbox("Simulation distribution", ["Normal", "Log-normal", "Gamma"])
    np.random.seed(42)
    # method-of-moments parameter estimation
    if dist_choice == "Normal":
        sim = np.random.normal(loc=mean, scale=std, size=int(n*1.2))
    elif dist_choice == "Log-normal":
        # estimate log-normal parameters
        var = std**2
        sigma2 = np.log(1 + var/mean**2)
        mu = np.log(mean) - 0.5*sigma2
        sigma = np.sqrt(sigma2)
        sim = np.random.lognormal(mean=mu, sigma=sigma, size=int(n*1.2))
    else:  # Gamma
        var = std**2
        shape = mean**2/var
        scale = var/mean
        sim = np.random.gamma(shape, scale, size=int(n*1.2))
    # truncate to bounds
    sim = sim[(sim >= pmin) & (sim <= pmax)]
    if sim.size < n:
        extra = np.random.uniform(pmin, pmax, size=n - sim.size)
        sim = np.hstack([sim, extra])
    payments = np.random.choice(sim, size=n, replace=False)

# Main single plot
st.pyplot(plot_dual(current_bm, proposed_bm, payments=payments,
                    window_sizes=window_dict, x_max_limit=x_axis_max))

# Flags

def flagged(val: float) -> bool:
    tier = tier_for_value(val)
    win  = window_dict[tier]
    return any(abs(val - inc) <= win for inc in INCREMENTS)

st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("Current flagged", "Yes" if flagged(current_bm) else "No")
col2.metric("Proposed flagged", "Yes" if flagged(proposed_bm) else "No")
