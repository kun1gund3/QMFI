import numpy as np
from scipy.stats import norm

def calculate_probit_weights(mu, n=1):
    """
    Berechnet die IRLS-Arbeitsgewichte für ein Probit-Modell (Binomial).
    W = (phi(Phi^-1(p)))^2 / (n * p * (1 - p))
    """
    if n <= 0:
        raise ValueError("n must be greater than 0")
    if not (0 < mu < n):
        # Probit benötigt strikte Grenzen, da PPF an den Rändern gegen Inf läuft
        return 0.0
        
    p = mu / n
    
    # 1. Bestimmung des linearen Prädiktors eta über die Quantilsfunktion (Phi^-1)
    eta = norm.ppf(p)
    
    # 2. Berechnung der Dichte an dieser Stelle (phi)
    phi = norm.pdf(eta)
    
    # 3. Analytisch komprimierte Gewichtsformel
    weights = (phi ** 2) / (n * p * (1 - p))
    return weights

# --- Beispielhafte Anwendung ---
mu_test = 0.6
gewichte_probit = calculate_probit_weights(mu_test, n=1)
print(f"Probit-Gewichte für mu={mu_test}: {gewichte_probit:.4f}")
