import streamlit as st

def load_theme():
    st.markdown(
        """
        <style>

        /* ===== Global ===== */
        html, body, [class*="css"] {
            background-color: #0b0f19;
            color: #e6f6ff;
            font-family: "Segoe UI", sans-serif;
        }

        /* ===== Titles ===== */
        h1, h2, h3 {
            color: #6ee7ff;
            text-shadow: 0 0 10px rgba(110,231,255,0.7);
        }

        /* ===== Tabs ===== */
        button[data-baseweb="tab"] {
            color: #9aeaff;
            font-weight: 500;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            border-bottom: 3px solid #00eaff;
        }

        /* ===== Buttons ===== */
        .stButton > button {
            background: linear-gradient(135deg, #00eaff, #0077ff);
            color: white;
            border-radius: 10px;
            border: 1px solid rgba(110,231,255,0.8);
            padding: 0.6em 1.4em;
            box-shadow:
                0 0 14px rgba(110,231,255,0.6),
                inset 0 0 6px rgba(255,255,255,0.25);
            transition: all 0.15s ease-in-out;
        }

        .stButton > button:hover {
            transform: scale(1.03);
            box-shadow:
                0 0 22px rgba(110,231,255,0.9),
                inset 0 0 8px rgba(255,255,255,0.35);
        }

        /* ===== Expanders ===== */
        .stExpander {
            border-radius: 14px;
            border: 1px solid rgba(110,231,255,0.45);
            box-shadow:
                0 0 20px rgba(110,231,255,0.3),
                inset 0 0 8px rgba(255,255,255,0.08);
        }

        /* ===== Text Inputs ===== */
        input[type="text"] {
            background-color: #0f172a;
            color: #e6f6ff;
            border: 1px solid rgba(110,231,255,0.6);
            border-radius: 8px;
            box-shadow: 0 0 8px rgba(110,231,255,0.35);
        }

        /* ===== Floating Info Badge ===== */
        .candidate-badge {
            position: fixed;
            top: 18px;
            right: 28px;
            padding: 8px 14px;
            background: rgba(15,23,42,0.85);
            border: 1px solid rgba(110,231,255,0.6);
            border-radius: 999px;
            color: #9aeaff;
            font-size: 14px;
            box-shadow: 0 0 14px rgba(110,231,255,0.5);
            z-index: 9999;
        }

        /* ===== Reset Button ===== */
        .reset-container {
            position: fixed;
            bottom: 18px;
            right: 28px;
            z-index: 9999;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
