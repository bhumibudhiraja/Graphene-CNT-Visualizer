import numpy as np
import matplotlib.pyplot as plt

def graphene_lattice(nx=6, ny=6, a=1.0):
    a1 = np.array([np.sqrt(3) * a, 0])
    a2 = np.array([np.sqrt(3)/2 * a, 3/2 * a])

    basis = [np.array([0, 0]), np.array([0, a])]

    points = []
    for i in range(nx):
        for j in range(ny):
            R = i * a1 + j * a2
            for b in basis:
                points.append(R + b)

    return np.array(points)

def draw_bonds(points, bond_length=1.0, tolerance=0.2):
    bonds = []
    n = len(points)
    for i in range(n):
        for j in range(i+1, n):
            dist = np.linalg.norm(points[i] - points[j])
            if abs(dist - bond_length) < tolerance:
                bonds.append((i, j))
    return bonds

def plot_graphene_structure(nx=8, ny=8):
    pts = graphene_lattice(nx=nx, ny=ny, a=1.0)
    bonds = draw_bonds(pts, bond_length=1.0, tolerance=0.2)

    plt.figure(figsize=(6, 6))
    for i, j in bonds:
        plt.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], linewidth=1)

    plt.scatter(pts[:, 0], pts[:, 1], s=60)
    plt.title("Graphene Structure (Atoms + Bonds)")
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.show()

def graphene_energy(kx, ky, t=1.0, a=1.0):
    term1 = 1
    term2 = 4 * np.cos(np.sqrt(3)*kx*a/2) * np.cos(ky*a/2)
    term3 = 4 * (np.cos(ky*a/2)**2)
    E = t * np.sqrt(term1 + term2 + term3)
    return E

def k_path(points, n_points=100):
    path = []
    for i in range(len(points)-1):
        start = np.array(points[i])
        end = np.array(points[i+1])
        for s in np.linspace(0, 1, n_points):
            path.append(start + s*(end-start))
    return np.array(path)

def plot_graphene_bandstructure():
    G = [0, 0]
    K = [4*np.pi/(3*np.sqrt(3)), 0]
    M = [np.pi/np.sqrt(3), np.pi/3]

    kpts = k_path([G, K, M, G], n_points=150)
    kx, ky = kpts[:, 0], kpts[:, 1]

    E = graphene_energy(kx, ky, t=1.0, a=1.0)

    plt.figure(figsize=(8, 5))
    plt.plot(E, label="Conduction (+E)")
    plt.plot(-E, label="Valence (-E)")

    total = len(kpts)
    ticks = [0, total//3, 2*total//3, total-1]
    plt.xticks(ticks, ["Γ", "K", "M", "Γ"])

    plt.axhline(0, linewidth=1, linestyle="--")
    plt.title("Graphene Band Structure")
    plt.xlabel("k-path (Γ → K → M → Γ)")
    plt.ylabel("Energy (arb units)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
