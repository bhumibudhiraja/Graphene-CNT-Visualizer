import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Import from your modules
from graphene_utils import graphene_lattice, draw_bonds, graphene_energy, k_path
from cnt_utils import cnt_type, cnt_diameter, cnt_bandgap
from cnt_analysis import generate_cnt_data

# ------------------------------------------------------------
# STREAMLIT CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Graphene + CNT Visualizer", layout="wide")

st.title("🧪 Graphene + CNT Structure & Band Visualizer")
st.write("An Electronics / VLSI mini-project tool to visualize graphene & CNT properties.")

# Sidebar menu
module = st.sidebar.selectbox(
    "Choose Module",
    ["Graphene", "CNT Chirality Analyzer", "CNT Band Structure", "CNT Eg vs Diameter"]
)

# ------------------------------------------------------------
# MODULE 1: GRAPHENE
# ------------------------------------------------------------
if module == "Graphene":
    st.subheader("Graphene Module")

    option = st.radio("Select Graph", ["Structure", "Band Structure"])

    # -------- Graphene Structure -------- #
    if option == "Structure":
        st.write("✅ Graphene honeycomb lattice visualization")

        col1, col2 = st.columns(2)
        with col1:
            nx = st.slider("nx (unit cells in X direction)", 2, 25, 8)
        with col2:
            ny = st.slider("ny (unit cells in Y direction)", 2, 25, 8)

        if st.button("Plot Graphene Structure"):
            pts = graphene_lattice(nx=nx, ny=ny, a=1.0)
            bonds = draw_bonds(pts, bond_length=1.0, tolerance=0.2)

            fig, ax = plt.subplots(figsize=(6, 6))

            for i, j in bonds:
                ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], linewidth=1)

            ax.scatter(pts[:, 0], pts[:, 1], s=60)
            ax.set_title(f"Graphene Structure ({nx} x {ny})")
            ax.axis("equal")
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

    # -------- Graphene Band Structure -------- #
    elif option == "Band Structure":
        st.write("✅ Graphene band structure (Γ → K → M → Γ)")

        if st.button("Plot Graphene Band Structure"):
            # High-symmetry points
            G = [0, 0]
            K = [4*np.pi/(3*np.sqrt(3)), 0]
            M = [np.pi/np.sqrt(3), np.pi/3]

            kpts = k_path([G, K, M, G], n_points=150)
            kx, ky = kpts[:, 0], kpts[:, 1]

            E = graphene_energy(kx, ky, t=1.0, a=1.0)

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.plot(E, label="Conduction (+E)")
            ax.plot(-E, label="Valence (-E)")

            total = len(kpts)
            ticks = [0, total//3, 2*total//3, total-1]
            ax.set_xticks(ticks)
            ax.set_xticklabels(["Γ", "K", "M", "Γ"])

            ax.axhline(0, linewidth=1, linestyle="--")
            ax.set_title("Graphene Band Structure")
            ax.set_xlabel("k-path (Γ → K → M → Γ)")
            ax.set_ylabel("Energy (arb units)")
            ax.grid(True, alpha=0.3)
            ax.legend()

            st.pyplot(fig)


# ------------------------------------------------------------
# MODULE 2: CNT CHIRALITY ANALYZER
# ------------------------------------------------------------
elif module == "CNT Chirality Analyzer":
    st.subheader("CNT Chirality Analyzer (n, m)")
    st.write("Enter CNT chirality values to determine metallic/semiconducting, diameter and bandgap.")

    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Enter n", min_value=1, max_value=60, value=10)
    with col2:
        m = st.number_input("Enter m", min_value=0, max_value=60, value=10)

    if st.button("Analyze CNT"):
        ttype = cnt_type(n, m)
        d = cnt_diameter(n, m)
        Eg = cnt_bandgap(n, m)

        if ttype == "Metallic":
            st.success(f"✅ CNT({n},{m}) is **METALLIC** (Eg ≈ 0)")
        else:
            st.success(f"✅ CNT({n},{m}) is **SEMICONDUCTING**")

        st.write(f"📏 **Diameter:** {d:.3f} nm")
        st.write(f"⚡ **Bandgap (Eg):** {Eg:.3f} eV")


# ------------------------------------------------------------
# MODULE 3: CNT BAND STRUCTURE
# ------------------------------------------------------------
elif module == "CNT Band Structure":
    st.subheader("CNT Band Structure Plot")
    st.write("Plots a simplified CNT band structure showing bandgap behavior.")

    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Enter n", min_value=1, max_value=60, value=10, key="cnt_n")
    with col2:
        m = st.number_input("Enter m", min_value=0, max_value=60, value=0, key="cnt_m")

    if st.button("Plot CNT Band Structure"):
        tube_type = cnt_type(n, m)
        Eg = cnt_bandgap(n, m)

        k = np.linspace(-np.pi, np.pi, 400)
        modes = 8

        fig, ax = plt.subplots(figsize=(8, 5))

        for q in range(-modes, modes + 1):
            shift = abs(q) * 0.3

            if tube_type == "Metallic":
                E = np.sqrt((k**2) + (shift**2))
            else:
                E = np.sqrt((k**2) + (shift**2) + (Eg/2)**2)

            ax.plot(k, E, linewidth=1)
            ax.plot(k, -E, linewidth=1)

        ax.axhline(0, linestyle="--", linewidth=1)
        ax.set_title(f"CNT Band Structure ({n},{m}) → {tube_type}")
        ax.set_xlabel("k (tube axis)")
        ax.set_ylabel("Energy (arb units)")
        ax.grid(True, alpha=0.3)

        if tube_type == "Semiconducting":
            ax.text(0.1, 0.5, f"Bandgap ≈ {Eg:.2f} eV", fontsize=10)

        st.pyplot(fig)


# ------------------------------------------------------------
# MODULE 4: CNT BANDGAP vs DIAMETER
# ------------------------------------------------------------
elif module == "CNT Eg vs Diameter":
    st.subheader("CNT Bandgap (Eg) vs Diameter Plot")
    st.write("Generates many CNTs and plots how bandgap changes with tube diameter.")

    nmax = st.slider("Max n value (generate CNTs up to n)", 5, 40, 20)

    if st.button("Generate Eg vs Diameter Plot"):
        diameters, bandgaps, types, labels = generate_cnt_data(n_max=nmax)

        semi_mask = (types == "Semiconducting")
        metal_mask = (types == "Metallic")

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.scatter(diameters[semi_mask], bandgaps[semi_mask], s=25, label="Semiconducting CNTs")
        ax.scatter(diameters[metal_mask], bandgaps[metal_mask], s=25, label="Metallic CNTs")

        ax.set_title("CNT Bandgap vs Diameter")
        ax.set_xlabel("Diameter (nm)")
        ax.set_ylabel("Bandgap Eg (eV)")
        ax.grid(True, alpha=0.3)
        ax.legend()

        st.pyplot(fig)

        st.info("✅ Observation: Smaller diameter CNTs generally have larger bandgap. Metallic CNTs show Eg ≈ 0.")
