import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from reliability.stopping_rule import (
    minimal_total_time_to_pass,
    extra_time_needed,
)

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Bayesian Stopping Rule (Poisson–Gamma)", layout="wide")
st.title("Bayesian Stopping Rule — Table + Curves + Accident → Extra Time")

with st.sidebar:
    st.header("Reliability Requirement")
    lam0 = st.number_input("λ₀ (target failure rate)", value=1e-3, format="%.6g")
    alpha = st.number_input("α (confidence = 1-α)", value=1e-2, format="%.6g")

    st.header("Prior (Gamma(a,b))")
    a = st.number_input("a (prior failures + 1)", value=1.0, min_value=1e-9)
    b = st.number_input("b (prior time credit)", value=0.0, min_value=0.0)

    st.header("Table Settings")
    r_max = st.slider("Max failures (r_max)", 0, 30, 10)

    st.header("Current / Accident State")
    r_current = st.number_input("Current failures r", value=1, min_value=0, step=1)
    T_current = st.number_input("Current total time T", value=2033.0, min_value=0.0)

# -------------------------
# Table computation
# -------------------------
rows = []
for r in range(0, r_max + 1):
    T_req = minimal_total_time_to_pass(lam0, alpha, r, a, b)
    rows.append(
        {
            "failures r": r,
            "required total time T": T_req,
            "extra time from now": max(0.0, T_req - T_current),
        }
    )
df = pd.DataFrame(rows)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Stopping-rule table")
    st.dataframe(df, width="stretch")

    dt = extra_time_needed(lam0, alpha, r_current, a, b, T_current)
    st.subheader("Accident → extra time needed")
    st.metric("ΔT (failure-free time needed)", f"{dt:.1f}")

with col2:
    st.subheader("Curve: required total time vs failures")
    fig = plt.figure()
    plt.plot(df["failures r"], df["required total time T"], marker="o")
    plt.xlabel("Number of failures (r)")
    plt.ylabel("Required total time T")
    plt.grid(True)
    st.pyplot(fig)
