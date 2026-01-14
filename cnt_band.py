import numpy as np
import matplotlib.pyplot as plt
from cnt_utils import cnt_type, cnt_bandgap

def plot_cnt_bandstructure(n, m, modes=8):
    """
    Simplified CNT band structure visualization
    - modes: number of quantized subbands to display
    """
    tube_type = cnt_type(n, m)
    Eg = cnt_bandgap(n, m)

    # k along nanotube axis
    k = np.linspace(-np.pi, np.pi, 400)

    plt.figure(figsize=(8, 5))

    # Generate multiple subbands
    for q in range(-modes, modes + 1):
        # quantized transverse energy shift
        shift = abs(q) * 0.3

        # If metallic, allow one band to cross 0
        if tube_type == "Metallic":
            E = np.sqrt((k**2) + (shift**2))
        else:
            # If semiconducting, enforce bandgap by adding Eg/2
            E = np.sqrt((k**2) + (shift**2) + (Eg/2)**2)

        plt.plot(k, E, linewidth=1)
        plt.plot(k, -E, linewidth=1)

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.title(f"CNT Band Structure for ({n},{m})  →  {tube_type}")
    plt.xlabel("k (along tube axis)")
    plt.ylabel("Energy (arb units)")
    plt.grid(True, alpha=0.3)

    if tube_type == "Semiconducting":
        plt.text(0.1, 0.5, f"Bandgap ≈ {Eg:.2f} eV", fontsize=10)

    plt.show()
