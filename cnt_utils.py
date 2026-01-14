import numpy as np

def cnt_diameter(n, m, a=0.246):
    """
    CNT diameter in nm (approx)
    a = graphene lattice constant in nm (~0.246 nm)
    """
    return (a / np.pi) * np.sqrt(n**2 + m**2 + n*m)

def cnt_type(n, m):
    """
    Classify CNT: metallic or semiconducting
    Rule: if (n-m)%3==0 -> metallic, else semiconducting
    """
    if (n - m) % 3 == 0:
        return "Metallic"
    return "Semiconducting"

def cnt_bandgap(n, m):
    """
    Approx CNT bandgap in eV (simplified)
    Metallic -> 0
    Semiconducting -> inversely proportional to diameter
    """
    t = 2.7  # eV (nearest-neighbor hopping energy)
    a_cc = 0.142  # nm (carbon-carbon bond length)

    tube_type = cnt_type(n, m)
    if tube_type == "Metallic":
        return 0.0

    d = cnt_diameter(n, m)  # nm
    Eg = (2 * a_cc * t) / d  # simplified formula
    return Eg
