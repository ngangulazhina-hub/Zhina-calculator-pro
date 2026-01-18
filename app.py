# app.py
import streamlit as st
import math

# ── Calculator Core Logic ────────────────────────────────────────────────
class ZhinaScientificCalculator:
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state.memory = 0.0

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    
    def divide(self, a, b):
        if b == 0:
            st.error("Division by zero!")
            return None
        return a / b

    def power(self, a, b): return a ** b
    
    def square_root(self, x):
        if x < 0:
            st.error("Cannot calculate square root of negative number")
            return None
        return math.sqrt(x)
    
    def memory_add(self, value):
        try:
            st.session_state.memory += float(value)
        except (ValueError, TypeError):
            st.warning("Cannot add to memory: invalid number")

    def memory_recall(self):
        return st.session_state.memory

    def memory_clear(self):
        st.session_state.memory = 0.0


# ── Safe-ish expression evaluation ───────────────────────────────────────
def safe_calculate(expression):
    """Very simple and limited eval - still not 100% safe for public apps"""
    expression = expression.replace('^', '**')  # allow ^ as power
    
    allowed_names = {
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "factorial": math.factorial
    }
    
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        if isinstance(result, complex):
            return "Complex numbers not supported"
        return float(result)
    except Exception as e:
        return f"Error: {str(e)}"


# ── Session state initialization ─────────────────────────────────────────
if 'current_input' not in st.session_state:
    st.session_state.current_input = "0"
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'calc' not in st.session_state:
    st.session_state.calc = ZhinaScientificCalculator()


# ── Button handler ───────────────────────────────────────────────────────
def handle_button(key):
    if key == "C":
        st.session_state.current_input = "0"
        st.session_state.expression = ""
        return

    if key == "=":
        full_expr = st.session_state.expression + st.session_state.current_input
        result = safe_calculate(full_expr)
        
        if isinstance(result, str) and "Error" in result:
            st.session_state.current_input = result
        else:
            st.session_state.current_input = str(result)
            st.session_state.expression = full_expr + " = "
        return

    # Operators
    if key in ["+", "-", "×", "÷", "^"]:
        op_map = {"×": "*", "÷": "/"}
        op = op_map.get(key, key)
        st.session_state.expression += st.session_state.current_input + op
        st.session_state.current_input = "0"
        return

    # Memory operations
    if key == "MR":
        st.session_state.current_input = str(st.session_state.calc.memory_recall())
        return
        
    if key == "M+":
        try:
            st.session_state.calc.memory_add(st.session_state.current_input)
            st.toast(f"Memory += {st.session_state.current_input}")
        except:
            st.toast("Cannot add to memory")
        return
        
    if key == "MC":
        st.session_state.calc.memory_clear()
        st.toast("Memory cleared")
        return

    # Square root (applied to current input)
    if key == "√":
        try:
            val = float(st.session_state.current_input)
            result = st.session_state.calc.square_root(val)
            if result is not None:
                st.session_state.current_input = str(result)
                st.session_state.expression = f"√({val}) = "
        except ValueError:
            st.session_state.current_input = "Error"
        return

    # Number / decimal input
    if key == ".":
        if "." not in st.session_state.current_input:
            st.session_state.current_input += "."
    else:
        # digits 0-9
        if st.session_state.current_input == "0" or st.session_state.current_input.startswith("Error"):
            st.session_state.current_input = key
        else:
            st.session_state.current_input += key


# ── Page layout & styling ────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="Zhina Calculator", layout="centered")

    # Modern dark + neon accent style (you can change this!)
    st.markdown("""
    <style>
        .stApp {
            

.stApp, .calculator-display, .main-display {
    direction: ltr !important;          /* Force left-to-right */
    unicode-bidi: plaintext !important; /* Prevent RTL flipping */
    text-align: right !important;
}

.main-display {
    color: #00eaff;
    font-size: 3.4rem;
    font-weight: bold;
    text-align: right !important;
    direction: ltr !important;
    unicode-bidi: embed !important;
    white-space: nowrap !important;     /* Prevent wrapping/line breaks */
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: 'Segoe UI', 'Courier New', monospace;
    letter-spacing: 1px;
}

.calculator-display {
    direction: ltr !important;
    text-align: right !important;
    min-width: 100%;                    /* Force full width */
}
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🧮 Zhina Scientific Calculator")

    # Display area
    with st.container():
        st.markdown(
            f"""
            <div class="calculator-display">
                <div class="expression">{st.session_state.expression}</div>
                <div class="main-display">{st.session_state.current_input}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Button layout
    buttons = [
        ["MC", "MR", "M+", "√"],
        ["C", "÷", "×", "-"],
        ["7", "8", "9", "+"],
        ["4", "5", "6", "^"],
        ["1", "2", "3", "="],
        ["0", ".", "="]  # last row special
    ]

    for i, row in enumerate(buttons):
        cols = st.columns([1]*4 if i < 5 else [2,1,1])
        
        for j, key in enumerate(row):
            if i == 5 and j == 0:  # wide 0 button
                cols[0].button("0", key="btn0", on_click=handle_button, args=("0",))
            elif i == 5 and j == 1:  # decimal
                cols[1].button(".", key="btn.", on_click=handle_button, args=(".",))
            elif i == 5 and j == 2:  # skip
                continue
            else:
                # normal buttons
                is_equal = (key == "=")
                cols[j if i<5 else j+1 if j>1 else j].button(
                    key,
                    key=f"btn{key}",
                    on_click=handle_button,
                    args=(key,),
                    type="primary" if is_equal else "secondary"
                )

    # Memory status
    st.markdown("---")
    st.caption(f"Memory: **{st.session_state.calc.memory_recall():.6g}**")


if __name__ == "__main__":
    main()
