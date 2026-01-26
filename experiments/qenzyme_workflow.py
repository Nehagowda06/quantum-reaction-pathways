import numpy as np
from scipy.linalg import expm
from hamiltonians.qenzyme import QEnzyme

MAX_STORE = 5
stored_simulations = []

def simulate(H, times, psi0):
    populations = []
    for t in times:
        U = expm(-1j * H * t)
        psi_t = U @ psi0
        populations.append(np.abs(psi_t)**2)
    return np.array(populations)

def metric_A(pop):  # Final product population
    return pop[-1, 3]

def metric_B(pop, times):  # Time to reach threshold
    threshold = 0.4
    for i, p in enumerate(pop[:, 3]):
        if p >= threshold:
            return times[i]
    return np.inf

def metric_C(pop):  # Selectivity
    return pop[-1, 3] / (np.sum(pop[-1, :3]) + 1e-9)

def metric_D(pop):  # Inhibition (lower is stronger)
    return 1.0 - pop[-1, 3]

def simulate_new():
    print("\nSimulating a new Hamiltonian...")

    enzyme = QEnzyme(
        tunneling_strength=float(input("Tunneling strength: ")),
        product_stabilization=float(input("Product stabilization: ")),
        ts_stabilization=float(input("TS stabilization: ")),
        environment_perturbation=float(input("Environment perturbation: "))
    )

    H = enzyme.hamiltonian()
    times = np.linspace(0, 10, 300)
    psi0 = np.zeros(4, dtype=complex)
    psi0[0] = 1.0

    pop = simulate(H, times, psi0)

    choice = input("Store this simulation? (y/n): ").lower()
    if choice == "y":
        if len(stored_simulations) >= MAX_STORE:
            print("❌ STACK OVERFLOW: Maximum stored simulations reached.")
            return

        name = input("Enter a name for this simulation: ")
        stored_simulations.append({
            "name": name,
            "pop": pop,
            "times": times
        })
        print(f"✅ Stored as '{name}'")
    else:
        print("🗑 Simulation discarded.")


def compare():
    if len(stored_simulations) < 2:
        print("⚠️ Need at least 2 stored simulations to compare.")
        return

    print("""
Choose metric:
1. Final product population
2. Time to reach product threshold
3. Selectivity
4. Inhibition efficiency
5. Combined (all metrics)
6. Exit
""")

    choice = input("Select: ")

    scores = {}

    for sim in stored_simulations:
        pop = sim["pop"]
        times = sim["times"]

        if choice == "1":
            score = metric_A(pop)
        elif choice == "2":
            score = -metric_B(pop, times)  # lower time = better
        elif choice == "3":
            score = metric_C(pop)
        elif choice == "4":
            score = -metric_D(pop)
        elif choice == "5":
            score = (
                metric_A(pop)
                - metric_B(pop, times)
                + metric_C(pop)
                - metric_D(pop)
            )
        else:
            return

        scores[sim["name"]] = score

    best = max(scores, key=scores.get)
    worst = min(scores, key=scores.get)

    print("\n📊 Comparison results:")
    for k, v in scores.items():
        print(f"{k}: {v:.3f}")

    print(f"\n🏆 BEST: {best}")
    print(f"❌ WORST: {worst}")

while True:
    print(f"""
Stored simulations: {len(stored_simulations)}/{MAX_STORE}

1. Simulate new Hamiltonian
2. Compare stored simulations
3. Exit
""")

    action = input("Choose an option: ")

    if action == "1":
        simulate_new()
    elif action == "2":
        compare()
    elif action == "3":
        print("Exiting.")
        break
