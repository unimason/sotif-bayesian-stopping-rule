# reliability/posterior.py

from scipy.stats import gamma

def posterior_cdf_lambda(lam0: float, r: int, T: float, a: float, b: float) -> float:
    """
    Prior:  λ ~ Gamma(a, b) (shape-rate)
    Posterior: λ | (r failures, total time T) ~ Gamma(a+r, b+T)
    Return: P(λ < lam0 | data)
    """
    shape = a + r
    rate = b + T
    if shape <= 0 or rate <= 0:
        raise ValueError("Invalid posterior parameters: ensure a+r>0 and b+T>0.")
    return gamma.cdf(lam0, a=shape, scale=1.0 / rate)