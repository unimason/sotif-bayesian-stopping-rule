# reliability/stopping_rule.py

from reliability.posterior import posterior_cdf_lambda

def minimal_total_time(
    r,
    lam0,
    alpha,
    prior,
    tol=1e-10,
    max_iter=200,
):
    """
    Find minimal total elapsed time T such that:
        P(λ < lam0 | r, T) >= 1 - alpha
    """
    target = 1.0 - alpha
    a = prior["a"]
    b = prior["b"]

    T_low, T_high = 0.0, 1.0

    # Bracket solution
    while posterior_cdf_lambda(lam0, r, T_high, a, b) < target:
        T_high *= 2.0
        if T_high > 1e9:
            return float("inf")

    # Bisection
    for _ in range(max_iter):
        T_mid = 0.5 * (T_low + T_high)
        if posterior_cdf_lambda(lam0, r, T_mid, a, b) >= target:
            T_high = T_mid
        else:
            T_low = T_mid

        if T_high - T_low < tol * max(1.0, T_high):
            break

    return T_high

def minimal_total_time_to_pass(
    lam0: float,
    alpha: float,
    r: int,
    a: float,
    b: float,
    tol: float = 1e-10,
    max_iter: int = 200,
    T_max: float = 1e12,
) -> float:
    """
    Find minimal total elapsed time T such that:
        P(λ < lam0 | r, T) >= 1 - alpha
    """
    target = 1.0 - alpha

    # If already pass at T=0? (rare; depends on prior)
    if posterior_cdf_lambda(lam0, r, 0.0, a, max(b, 1e-12)) >= target:
        return 0.0

    T_low, T_high = 0.0, 1.0
    # Bracket
    while posterior_cdf_lambda(lam0, r, T_high, a, b) < target:
        T_high *= 2.0
        if T_high > T_max:
            raise RuntimeError("Cannot bracket solution: try larger T_max or adjust parameters.")

    # Bisection
    for _ in range(max_iter):
        T_mid = 0.5 * (T_low + T_high)
        if posterior_cdf_lambda(lam0, r, T_mid, a, b) >= target:
            T_high = T_mid
        else:
            T_low = T_mid
        if T_high - T_low < tol * max(1.0, T_high):
            break

    return T_high

def accident_to_extra_time(
    lam0: float,
    alpha: float,
    a: float,
    b: float,
    r_current: int,
    T_current: float,
) -> float:
    """
    Given current state (r_current failures, total elapsed time T_current),
    return extra failure-free time needed to pass stopping rule.

    This is the direct "补测多久" interface.
    """
    T_req = minimal_total_time_to_pass(lam0, alpha, r_current, a, b)
    return max(0.0, T_req - T_current)


def extra_time_needed(
    lam0: float,
    alpha: float,
    r_current: int,
    a: float,
    b: float,
    T_current: float,
) -> float:
    """
    Backward-compatible alias used by UI scripts.
    """
    return accident_to_extra_time(lam0, alpha, a, b, r_current, T_current)
