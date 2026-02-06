# reliability/plotting.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

def plot_required_time_vs_failures(r_values, T_values, label):
    plt.plot(r_values, T_values, marker="o", label=label)

def plot_posterior_pdf(lam_grid, r, T, prior, label):
    a = prior["a"]
    b = prior["b"]

    shape = a + r
    rate = b + T
    pdf = gamma.pdf(lam_grid, a=shape, scale=1.0 / rate)
    plt.plot(lam_grid, pdf, label=label)