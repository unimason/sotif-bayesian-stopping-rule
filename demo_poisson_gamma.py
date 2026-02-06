# demo_poisson_gamma.py

import numpy as np
import matplotlib.pyplot as plt

from reliability.priors import gamma_prior
from reliability.stopping_rule import minimal_total_time
from reliability.plotting import (
    plot_required_time_vs_failures,
    plot_posterior_pdf,
)

# Paper-like requirement
lambda_0 = 1e-3
alpha = 0.01

priors = [
    (gamma_prior(1, 0), "a=1, b=0 (paper-like)"),
    (gamma_prior(1, 1000), "a=1, b=1000 (prior time)"),
    (gamma_prior(3, 0), "a=3, b=0 (prior failures)"),
    (gamma_prior(3, 2000), "a=3, b=2000 (time + failures)"),
]

# -------- Plot 1 --------
r_values = list(range(0, 11))

plt.figure()
for prior, label in priors:
    T_values = [
        minimal_total_time(r, lambda_0, alpha, prior)
        for r in r_values
    ]
    plot_required_time_vs_failures(r_values, T_values, label)

plt.title("Required total time vs failures")
plt.xlabel("Number of failures (r)")
plt.ylabel("Total elapsed time T")
plt.grid(True)
plt.legend()
plt.show()

# -------- Plot 2 --------
r_obs = 1
T_obs = 2000.0
lam_grid = np.linspace(0, 0.004, 800)

plt.figure()
for prior, label in priors:
    plot_posterior_pdf(lam_grid, r_obs, T_obs, prior, label)

plt.axvline(lambda_0, linestyle="--")
plt.title(f"Posterior PDF of λ (r={r_obs}, T={T_obs})")
plt.xlabel("λ")
plt.ylabel("Density")
plt.grid(True)
plt.legend()
plt.show()