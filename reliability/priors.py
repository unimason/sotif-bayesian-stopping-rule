# reliability/priors.py

def gamma_prior(a=1.0, b=0.0):
    """
    Gamma prior for failure rate λ.
    a: shape (a-1 virtual failures)
    b: rate  (b virtual time)
    """
    return {"a": a, "b": b}