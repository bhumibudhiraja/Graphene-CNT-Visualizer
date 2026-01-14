from graphene_utils import plot_graphene_structure, plot_graphene_bandstructure
from cnt_utils import cnt_type, cnt_diameter, cnt_bandgap
from cnt_band import plot_cnt_bandstructure

print("\n===== GRAPHENE + CNT VISUALIZER =====")
print("1) Plot Graphene Structure")
print("2) Plot Graphene Band Structure")
print("3) CNT Chirality Analyzer (n,m)")
print("4) Plot CNT Band Structure")

choice = input("Enter choice: ")

if choice == "1":
    plot_graphene_structure()

elif choice == "2":
    plot_graphene_bandstructure()

elif choice == "3":
    n = int(input("Enter n: "))
    m = int(input("Enter m: "))

    ttype = cnt_type(n, m)
    d = cnt_diameter(n, m)
    Eg = cnt_bandgap(n, m)

    print("\n--- CNT RESULTS ---")
    print(f"CNT (n,m) = ({n},{m})")
    print(f"Type      = {ttype}")
    print(f"Diameter  = {d:.3f} nm")
    print(f"Bandgap   = {Eg:.3f} eV")

elif choice == "4":
    n = int(input("Enter n: "))
    m = int(input("Enter m: "))
    plot_cnt_bandstructure(n, m)

else:
    print("Invalid choice!")
