import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from hamiltonians.qenzyme import QEnzyme


def generate_page():

    st.header("🧪 Generate Candidate Hamiltonian")
    st.caption(
        "Define a quantum-effective enzyme Hamiltonian and simulate its "
        "reaction pathway via first-principles quantum dynamics."
    )

    st.markdown("---")
    
    with st.expander("⚙️ Control Panel", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            tunneling = st.slider(
                "Tunneling strength",
                min_value=0.1,
                max_value=2.0,
                value=1.0,
                help="Controls quantum tunneling along the reaction coordinate."
            )

            ts = st.slider(
                "Transition-state stabilization",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                help="Stabilization of the transition region."
            )

        with col2:
            bias = st.slider(
                "Product stabilization",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                help="Energetic stabilization of the product state."
            )

            env = st.slider(
                "Environmental perturbation",
                min_value=0.0,
                max_value=0.5,
                value=0.1,
                help="Environmental / electrostatic perturbation."
            )

    st.markdown("")
   
    if st.button("Generate & Simulate", type="primary"):
        enzyme = QEnzyme(
            tunneling=tunneling,
            bias=bias,
            ts_stabilization=ts,
            environment=env,
        )

        times = np.linspace(0, 10, 300)
        populations = enzyme.simulate(times)
        st.session_state.last_simulation = {
            "times": times,
            "pop": populations,
            "params": (tunneling, bias, ts, env),
        }
   
    if st.session_state.last_simulation is not None:
        sim = st.session_state.last_simulation

        st.markdown("### Quantum Reaction Pathway")

        fig, ax = plt.subplots(figsize=(7.5, 4.5))

        labels = [
            "Reactant |0⟩",
            "Transition (left) |1⟩",
            "Transition (right) |2⟩",
            "Product |3⟩",
        ]

        for i in range(4):
            ax.plot(sim["times"], sim["pop"][:, i], label=labels[i])

        ax.set_xlabel("Time")
        ax.set_ylabel("Population")
        ax.legend()
        ax.grid(alpha=0.25)

        st.pyplot(fig, use_container_width=True)
        st.markdown("### Save or discard this simulation")

        name = st.text_input(
            "Candidate name",
            placeholder="e.g. Fast-Catalyst-A",
            key="candidate_name",
        )

        col_store, col_discard = st.columns(2)

        with col_store:
            if st.button("Store candidate"):
                if not name.strip():
                    st.warning("Please provide a candidate name.")
                elif len(st.session_state.candidates) >= 5:
                    st.warning("Maximum of 5 candidates allowed.")
                else:
                    st.session_state.candidates.append({
                        "name": name.strip(),
                        "times": sim["times"],
                        "pop": sim["pop"],
                        "params": sim["params"],
                    })
                    st.session_state.last_simulation = None
                    st.rerun()

        with col_discard:
            if st.button("Discard simulation"):
                st.session_state.last_simulation = None
                st.rerun()
