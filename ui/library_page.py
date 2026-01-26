import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def library_page():
   
    st.header("📚 Candidate Library")
    st.caption(
        "Stored candidate Hamiltonians and their simulated quantum reaction pathways. "
        "Expand each candidate to inspect detailed dynamics."
    )

    st.markdown("---")
    
    if not st.session_state.candidates:
        st.info(
            "No candidates stored yet. "
            "Generate and store at least one candidate to view it here."
        )
        return
    for idx, candidate in enumerate(list(st.session_state.candidates)):
        name = candidate["name"]
        params = candidate["params"]
        times = candidate["times"]
        pop = candidate["pop"]
        
        final_product = pop[-1, 3]
        max_product = np.max(pop[:, 3])
        variance_product = np.var(pop[:, 3])

        with st.expander(f"{idx + 1}. {name}", expanded=False):
            
            st.markdown("**Hamiltonian parameters**")

            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            col_p1.metric("Tunneling", f"{params[0]:.2f}")
            col_p2.metric("Product bias", f"{params[1]:.2f}")
            col_p3.metric("TS stabilization", f"{params[2]:.2f}")
            col_p4.metric("Environment", f"{params[3]:.2f}")

            st.markdown("")
            
            fig, ax = plt.subplots(figsize=(7.5, 4.5))

            labels = [
                "Reactant |0⟩",
                "Transition (left) |1⟩",
                "Transition (right) |2⟩",
                "Product |3⟩"
            ]

            for i in range(4):
                ax.plot(times, pop[:, i], label=labels[i])

            ax.set_xlabel("Time")
            ax.set_ylabel("Population")
            ax.set_title("Quantum Reaction Pathway")
            ax.legend()
            ax.grid(alpha=0.25)

            st.pyplot(fig, use_container_width=True)
            st.markdown("**Product state evolution (|3⟩)**")

            fig2, ax2 = plt.subplots(figsize=(7.5, 1.8))
            ax2.plot(times, pop[:, 3])
            ax2.set_ylabel("Population")
            ax2.set_xlabel("Time")
            ax2.grid(alpha=0.25)

            st.pyplot(fig2, use_container_width=True)
            
            if st.button(
                f"Remove candidate: {name}",
                key=f"delete_{idx}"
            ):
                st.session_state.candidates.pop(idx)
                st.rerun()
