import streamlit as st
import sympy as sp
from sympy.parsing.latex import parse_latex
import re

# === BEAUTIFUL THEME & FONT ===
st.set_page_config(page_title="Zhina Calculator Pro", layout="centered")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');
    .css-1d391kg {font-family: 'Orbitron', monospace !important;}
    .stApp {background: linear-gradient(135deg, #1a0033, #4a148c); color: #e0e0ff;}
    .stButton>button {background: #7e57c2; color: white; border-radius: 12px; font-size: 20px; padding: 15px;}
    .result {font-size: 48px; color: #ffeb3b; text-align: center; margin: 20px; font-weight: bold;}
    .step {background: rgba(126, 87, 194, 0.3); padding: 10px; border-radius: 10px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Zhina Calculator Pro")
st.caption("AI Math Tutor • Step-by-Step • Scientific • Beautiful")

# Tabs
tab1, tab2, tab3 = st.tabs(["🧮 Calculator", "🤖 AI Math Helper", "📊 History"])

# === TAB 1: SCIENTIFIC CALCULATOR ===
with tab1:
    st.markdown("<div class='result'>0</div>", unsafe_allow_html=True)
    cols = st.columns(5)
    buttons = [
        ['C', '(', ')', '÷'],
        ['sin', 'cos', 'tan', '×'],
        ['7', '8', '9', '-'],
        ['4', '5', '6', '+'],
        ['1', '2', '3', '='],
        ['0', '.', 'π', '^']
    ]
    for row in buttons:
        cols = st.columns(5)
        for i, btn in enumerate(row):
            if cols[i].button(btn, key=btn):
                st.session_state.input = st.session_state.get('input', '') + btn

# === TAB 2: AI MATH HELPER (Step-by-Step) ===
with tab2:
    st.markdown("### Ask any math question — I’ll solve it step by step")
    question = st.text_input("Example: Solve x² + 5x + 6 = 0", placeholder="Type or paste your math problem")
    
    if st.button("Solve with Steps"):
        with st.spinner("Zhina is solving..."):
            try:
                # Try LaTeX first, then plain text
                expr = parse_latex(question) if "frac" in question or "^" in question else sp.sympify(question.replace('=', '-(') + ')')
                solution = sp.solve(expr, dict=True)
                steps = sp.latex(expr) + " = 0"
                for sol in solution:
                    st.markdown(f"<div class='step'>→ {sol}</div>", unsafe_allow_html=True)
                st.success("Solved by Zhina AI")
            except:
                st.info("Try: x^2 + 5x + 6 = 0  or  integrate sin(x)")

# === TAB 3: HISTORY ===
with tab3:
    st.write("Coming soon — your calculation history")

st.markdown("<center>Made with 💜 by Zhina AI</center>", unsafe_allow_html=True)
