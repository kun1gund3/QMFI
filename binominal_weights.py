import numpy as np

def calculate_optimized_binomial_weights(mu, n=1):
    """
    Optimierte und numerisch stabile Berechnung der Gewichte.
    Nutzt die analytische Kürzung des Terms W = p * (1 - p) / n,
    um Divisionen durch Null inhärent zu vermeiden.
    """
    if n <= 0:
        raise ValueError("n must be greater than 0")
    if not (0 <= mu <= n):
        raise ValueError("mu must be within the interval [0, n]")
        
    p = mu / n
    # Analytisch gekürzte Formel (verhindert Division durch Null im Zwischenschritt)
    return (p * (1 - p)) / n

# --- Beispielhafte Anwendung ---
mu_test = 0.6
gewichte = calculate_optimized_binomial_weights(mu_test, n=1)
print(f"Optimierte Gewichte für mu={mu_test}: {gewichte:.4f}")

