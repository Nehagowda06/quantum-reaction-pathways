import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def screen_page():
    st.header("📊 Screen & Rank Candidates")
    st.caption(
        "Compare stored candidate Hamiltonians under different physically meaningful "
        "efficiency metrics to identify optimal reaction pathways."
    )

    st.markdown("---")
    if len(st.session_state.candidates) < 2:
        st.info(
            "At least **two stored candidates** are required to perform screening. "
            "Generate and store additional candidates to proceed."
        )
        return
    st.subheader("🔍 Select Screening Metric")

    metric = st.selectbox(
        "Efficiency criterion",
        [
            "Final product yield",
            "Reaction speed",
            "Selectivity",
            "Dynamical stability",
            "Composite score"
        ]
    )
    with st.expander("ℹ️ What does this metric mean?", expanded=True):

        if metric == "Final product yield":
            st.write(
                "Measures the final population of the product state |3⟩. "
                "This metric is appropriate when maximizing overall conversion "
                "or yield is the primary objective."
            )

        elif metric == "Reaction speed":
            st.write(
                "Measures how quickly the product population reaches a predefined threshold. "
                "This metric is useful when reaction kinetics or fast response is critical."
            )

        elif metric == "Selectivity":
            st.write(
                "Compares product population relative to intermediate or competing states. "
                "This metric is relevant when minimizing side pathways is important."
            )

        elif metric == "Dynamical stability":
            st.write(
                "Assesses fluctuations in product population over time. "
                "Lower variance indicates more robust and stable reaction dynamics."
            )

        else:
            st.write(
                "Combines yield, speed, and stability into a single composite score. "
                "This metric provides a balanced assessment when no single criterion dominates."
            )

    st.markdown("")
    scores = []

    for candidate in st.session_state.candidates:
        name = candidate["name"]
        pop = candidate["pop"]
        times = candidate["times"]

        final_product = pop[-1, 3]
        variance_product = np.var(pop[:, 3])
        threshold = 0.4
        try:
            speed_index = next(
                i for i, p in enumerate(pop[:, 3]) if p >= threshold
            )
            speed_score = -times[speed_index]
        except StopIteration:
            speed_score = -np.inf

        if metric == "Final product yield":
            score = final_product

        elif metric == "Reaction speed":
            score = speed_score

        elif metric == "Selectivity":
            score = final_product / (np.sum(pop[-1, :3]) + 1e-9)

        elif metric == "Dynamical stability":
            score = -variance_product

        else:
            score = (
                final_product
                + speed_score * 0.3
                - variance_product * 0.2
            )

        scores.append({
            "Candidate": name,
            "Score": score,
            "Final yield": final_product,
            "Stability": variance_product
        })

    df = pd.DataFrame(scores).sort_values(
        by="Score", ascending=False
    ).reset_index(drop=True)

    best = df.iloc[0]["Candidate"]
    worst = df.iloc[-1]["Candidate"]
    st.subheader("🏆 Ranking Results")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        f"""
        **Best candidate:** `{best}`  
        **Least effective candidate:** `{worst}`
        """
    )

    st.markdown("---")
    st.subheader("📈 Product Population Comparison")

    fig, ax = plt.subplots(figsize=(8.5, 5))

    for candidate in st.session_state.candidates:
        name = candidate["name"]
        pop = candidate["pop"]
        times = candidate["times"]

        ax.plot(
            times,
            pop[:, 3],
            label=name,
            linewidth=2 if name == best else 1.2,
            alpha=0.95 if name == best else 0.6
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("Product population |3⟩")
    ax.set_title("Emergent Reaction Pathways under Different Hamiltonians")
    ax.legend()
    ax.grid(alpha=0.25)

    st.pyplot(fig, use_container_width=True)
    st.markdown("### 🧠 Interpretation")

    st.write(
        f"The screening results indicate that **{best}** most effectively "
        f"drives population transfer toward the product state under the selected "
        f"efficiency criterion. Conversely, **{worst}** exhibits comparatively "
        f"weaker catalytic performance."
    )

    st.write(
        "These differences emerge purely from changes in the effective Hamiltonian, "
        "demonstrating how quantum mechanical structure directly shapes reaction pathways."
    )
