import streamlit as st
import math

# --- 1. Core Calculator Logic (Unchanged) ---

class ZhinaScientificCalculator:
    """Core mathematical logic for the Zhina Scientific Calculator."""
    # ... (All methods are the same: add, subtract, multiply, divide, power, sqrt, log, memory_add/recall/clear)
    # ... (Retaining the original methods for brevity in the re-check)
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state.memory = 0

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            st.error("Error: Cannot divide by zero.")
            return None
        return a / b

    def square_root(self, x):
        if x < 0:
            st.error("Error: Cannot take the square root of a negative number.")
            return None
        return math.sqrt(x)
    
    # ... (other scientific functions omitted for brevity in the re-check)

    def memory_add(self, value):
        st.session_state.memory += value
    def memory_recall(self):
        return st.session_state.memory
    def memory_clear(self):
        st.session_state.memory = 0
        
# --- 2. Calculation Function (Using eval() for simplicity, but acknowledge the risk) ---

def calculate(full_expression):
    """
    ATTENTION: This function uses eval() for simplicity. 
    REPLACE THIS with a safer library (like NumExpr) for production use.
    """
    # Simple string substitutions to handle basic scientific notation if needed
    full_expression = full_expression.replace('^', '**')

    try:
        # **The Vulnerable Line - Use with Caution**
        result = eval(full_expression) 
        return str(result)
    except Exception as e:
        return "Error"


# --- 3. Streamlit Application Interface (Refined) ---

# Initialize state variables
if 'current_input' not in st.session_state:
    st.session_state.current_input = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'calc' not in st.session_state:
    st.session_state.calc = ZhinaScientificCalculator()


def handle_button(key):
    """Updates the input based on the button pressed."""
    
    # --- Clear/Equals ---
    if key == 'C':
        st.session_state.current_input = '0'
        st.session_state.expression = ''
        return
    
    if key == '=':
        full_expression = st.session_state.expression + st.session_state.current_input
        result_str = calculate(full_expression)
        
        # Update display
        if result_str == "Error":
             st.session_state.expression = ''
        else:
             st.session_state.expression = full_expression + '='
        
        st.session_state.current_input = result_str
        return

    # --- Operators ---
    if key in ['+', '-', '*', '/']:
        # Append current number and operator to the expression
        st.session_state.expression += st.session_state.current_input + key
        st.session_state.current_input = '0'
        return

    # --- Memory Keys ---
    if key == 'MR':
        st.session_state.current_input = str(st.session_state.calc.memory_recall())
        return
    if key == 'M+':
        try:
            # Only add the current number input, not the whole expression result
            st.session_state.calc.memory_add(float(st.session_state.current_input))
            st.toast(f"Added {st.session_state.current_input} to Memory ({st.session_state.calc.memory_recall():.4f})")
        except ValueError:
             st.toast("Invalid value for M+")
        return
    if key == 'MC':
        st.session_state.calc.memory_clear()
        st.toast("Memory Cleared!")
        return

    # --- Scientific Functions (Directly call the method) ---
    if key == 'sqrt':
        try:
            current_value = float(st.session_state.current_input)
            result = st.session_state.calc.square_root(current_value)
            
            if result is not None:
                st.session_state.current_input = str(result)
                st.session_state.expression = f"sqrt({current_value})=" # Show function in expression
        except ValueError:
            st.session_state.current_input = "Error"
        return

    # --- Standard Keys (0-9, .) ---
    if st.session_state.current_input == '0' or st.session_state.current_input == "Error":
        # Clear '0' or 'Error' when a new digit is pressed
        if key == '.':
             st.session_state.current_input = '0.'
        else:
            st.session_state.current_input = key
    elif key == '.' and '.' in st.session_state.current_input:
        pass # Only one decimal point allowed
    else:
        st.session_state.current_input += key


def main():
    st.set_page_config(page_title="Zhina Calculator", layout="centered")
    
    # ... (The custom CSS styling remains the same)
    st.markdown("""
        <style>
        /* General Streamlit tweaks for a calculator feel */
        .stButton>button {
            width: 100%;
            height: 70px; /* Large buttons */
            font-size: 24px;
            margin: 2px 0;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        /* Style for the display area */
        .expression-display {
            text-align: right;
            font-size: 16px;
            color: #888;
            height: 20px;
        }
        .input-display {
            text-align: right;
            font-size: 48px;
            margin-bottom: 10px;
            height: 60px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Zhina Scientific Calculator")
    
    # --- Display Area ---
    st.markdown(f'<div class="expression-display">{st.session_state.expression}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="input-display">{st.session_state.current_input}</div>', unsafe_allow_html=True)

    # Define the button layout
    r1 = ['MC', 'MR', 'M+', 'sqrt']
    r2 = ['C', '/', '*', '-'] 
    r3 = ['7', '8', '9', '+']
    r4 = ['4', '5', '6']
    r5 = ['1', '2', '3']
    r6 = ['0', '.', '=']

    # --- Button Grid ---
    
    # ... (The button layout logic is the same: R1, R2, R3, R4, R5, R6)
    for row_keys in [r1, r2, r3, r4, r5]:
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        for i, key in enumerate(row_keys):
            cols[i].button(key, key=key, on_click=handle_button, args=(key,))
            
    # Final Row (R6) - '0', '.', '='
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1]) 
    col1.button('0', key='0', on_click=handle_button, args=('0',))
    col2.button('.', key='.', on_click=handle_button, args=('.',))
    col4.button('=', key='=', on_click=handle_button, args=('=',)) 
    
    # Display Memory Status
    st.markdown("---")
    st.info(f"Memory (MR/M+): **{st.session_state.calc.memory_recall():.4f}**")

if __name__ == '__main__':
    main()
import streamlit as st
import math

# --- 1. Core Calculator Logic (Unchanged) ---

class ZhinaScientificCalculator:
    """Core mathematical logic for the Zhina Scientific Calculator."""
    # ... (All methods are the same: add, subtract, multiply, divide, power, sqrt, log, memory_add/recall/clear)
    # ... (Retaining the original methods for brevity in the re-check)
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state.memory = 0

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            st.error("Error: Cannot divide by zero.")
            return None
        return a / b

    def square_root(self, x):
        if x < 0:
            st.error("Error: Cannot take the square root of a negative number.")
            return None
        return math.sqrt(x)
    
    # ... (other scientific functions omitted for brevity in the re-check)

    def memory_add(self, value):
        st.session_state.memory += value
    def memory_recall(self):
        return st.session_state.memory
    def memory_clear(self):
        st.session_state.memory = 0
        
# --- 2. Calculation Function (Using eval() for simplicity, but acknowledge the risk) ---

def calculate(full_expression):
    """
    ATTENTION: This function uses eval() for simplicity. 
    REPLACE THIS with a safer library (like NumExpr) for production use.
    """
    # Simple string substitutions to handle basic scientific notation if needed
    full_expression = full_expression.replace('^', '**')

    try:
        # **The Vulnerable Line - Use with Caution**
        result = eval(full_expression) 
        return str(result)
    except Exception as e:
        return "Error"


# --- 3. Streamlit Application Interface (Refined) ---

# Initialize state variables
if 'current_input' not in st.session_state:
    st.session_state.current_input = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'calc' not in st.session_state:
    st.session_state.calc = ZhinaScientificCalculator()


def handle_button(key):
    """Updates the input based on the button pressed."""
    
    # --- Clear/Equals ---
    if key == 'C':
        st.session_state.current_input = '0'
        st.session_state.expression = ''
        return
    
    if key == '=':
        full_expression = st.session_state.expression + st.session_state.current_input
        result_str = calculate(full_expression)
        
        # Update display
        if result_str == "Error":
             st.session_state.expression = ''
        else:
             st.session_state.expression = full_expression + '='
        
        st.session_state.current_input = result_str
        return

    # --- Operators ---
    if key in ['+', '-', '*', '/']:
        # Append current number and operator to the expression
        st.session_state.expression += st.session_state.current_input + key
        st.session_state.current_input = '0'
        return

    # --- Memory Keys ---
    if key == 'MR':
        st.session_state.current_input = str(st.session_state.calc.memory_recall())
        return
    if key == 'M+':
        try:
            # Only add the current number input, not the whole expression result
            st.session_state.calc.memory_add(float(st.session_state.current_input))
            st.toast(f"Added {st.session_state.current_input} to Memory ({st.session_state.calc.memory_recall():.4f})")
        except ValueError:
             st.toast("Invalid value for M+")
        return
    if key == 'MC':
        st.session_state.calc.memory_clear()
        st.toast("Memory Cleared!")
        return

    # --- Scientific Functions (Directly call the method) ---
    if key == 'sqrt':
        try:
            current_value = float(st.session_state.current_input)
            result = st.session_state.calc.square_root(current_value)
            
            if result is not None:
                st.session_state.current_input = str(result)
                st.session_state.expression = f"sqrt({current_value})=" # Show function in expression
        except ValueError:
            st.session_state.current_input = "Error"
        return

    # --- Standard Keys (0-9, .) ---
    if st.session_state.current_input == '0' or st.session_state.current_input == "Error":
        # Clear '0' or 'Error' when a new digit is pressed
        if key == '.':
             st.session_state.current_input = '0.'
        else:
            st.session_state.current_input = key
    elif key == '.' and '.' in st.session_state.current_input:
        pass # Only one decimal point allowed
    else:
        st.session_state.current_input += key


def main():
    st.set_page_config(page_title="Zhina Calculator", layout="centered")
    
    # ... (The custom CSS styling remains the same)
    st.markdown("""
        <style>
        /* General Streamlit tweaks for a calculator feel */
        .stButton>button {
            width: 100%;
            height: 70px; /* Large buttons */
            font-size: 24px;
            margin: 2px 0;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        /* Style for the display area */
        .expression-display {
            text-align: right;
            font-size: 16px;
            color: #888;
            height: 20px;
        }
        .input-display {
            text-align: right;
            font-size: 48px;
            margin-bottom: 10px;
            height: 60px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Zhina Scientific Calculator")
    
    # --- Display Area ---
    st.markdown(f'<div class="expression-display">{st.session_state.expression}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="input-display">{st.session_state.current_input}</div>', unsafe_allow_html=True)

    # Define the button layout
    r1 = ['MC', 'MR', 'M+', 'sqrt']
    r2 = ['C', '/', '*', '-'] 
    r3 = ['7', '8', '9', '+']
    r4 = ['4', '5', '6']
    r5 = ['1', '2', '3']
    r6 = ['0', '.', '=']

    # --- Button Grid ---
    
    # ... (The button layout logic is the same: R1, R2, R3, R4, R5, R6)
    for row_keys in [r1, r2, r3, r4, r5]:
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        for i, key in enumerate(row_keys):
            cols[i].button(key, key=key, on_click=handle_button, args=(key,))
            
    # Final Row (R6) - '0', '.', '='
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1]) 
    col1.button('0', key='0', on_click=handle_button, args=('0',))
import streamlit as st
import math

# --- 1. Core Calculator Logic (Unchanged) ---

class ZhinaScientificCalculator:
    """Core mathematical logic for the Zhina Scientific Calculator."""
    # ... (All methods are the same: add, subtract, multiply, divide, power, sqrt, log, memory_add/recall/clear)
    # ... (Retaining the original methods for brevity in the re-check)
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state.memory = 0

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            st.error("Error: Cannot divide by zero.")
            return None
        return a / b

    def square_root(self, x):
        if x < 0:
            st.error("Error: Cannot take the square root of a negative number.")
            return None
        return math.sqrt(x)
    
    # ... (other scientific functions omitted for brevity in the re-check)

    def memory_add(self, value):
        st.session_state.memory += value
    def memory_recall(self):
        return st.session_state.memory
    def memory_clear(self):
        st.session_state.memory = 0
        
# --- 2. Calculation Function (Using eval() for simplicity, but acknowledge the risk) ---

def calculate(full_expression):
    """
    ATTENTION: This function uses eval() for simplicity. 
    REPLACE THIS with a safer library (like NumExpr) for production use.
    """
    # Simple string substitutions to handle basic scientific notation if needed
    full_expression = full_expression.replace('^', '**')

    try:
        # **The Vulnerable Line - Use with Caution**
        result = eval(full_expression) 
        return str(result)
    except Exception as e:
        return "Error"


# --- 3. Streamlit Application Interface (Refined) ---

# Initialize state variables
if 'current_input' not in st.session_state:
    st.session_state.current_input = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'calc' not in st.session_state:
    st.session_state.calc = ZhinaScientificCalculator()


def handle_button(key):
    """Updates the input based on the button pressed."""
    
    # --- Clear/Equals ---
    if key == 'C':
        st.session_state.current_input = '0'
        st.session_state.expression = ''
        return
    
    if key == '=':
        full_expression = st.session_state.expression + st.session_state.current_input
        result_str = calculate(full_expression)
        
        # Update display
        if result_str == "Error":
             st.session_state.expression = ''
        else:
             st.session_state.expression = full_expression + '='
        
        st.session_state.current_input = result_str
        return

    # --- Operators ---
    if key in ['+', '-', '*', '/']:
        # Append current number and operator to the expression
        st.session_state.expression += st.session_state.current_input + key
        st.session_state.current_input = '0'
        return

    # --- Memory Keys ---
    if key == 'MR':
        st.session_state.current_input = str(st.session_state.calc.memory_recall())
        return
    if key == 'M+':
        try:
            # Only add the current number input, not the whole expression result
            st.session_state.calc.memory_add(float(st.session_state.current_input))
            st.toast(f"Added {st.session_state.current_input} to Memory ({st.session_state.calc.memory_recall():.4f})")
        except ValueError:
             st.toast("Invalid value for M+")
        return
    if key == 'MC':
        st.session_state.calc.memory_clear()
        st.toast("Memory Cleared!")
        return

    # --- Scientific Functions (Directly call the method) ---
    if key == 'sqrt':
        try:
            current_value = float(st.session_state.current_input)
            result = st.session_state.calc.square_root(current_value)
            
            if result is not None:
                st.session_state.current_input = str(result)
                st.session_state.expression = f"sqrt({current_value})=" # Show function in expression
        except ValueError:
            st.session_state.current_input = "Error"
        return

    # --- Standard Keys (0-9, .) ---
    if st.session_state.current_input == '0' or st.session_state.current_input == "Error":
        # Clear '0' or 'Error' when a new digit is pressed
        if key == '.':
             st.session_state.current_input = '0.'
        else:
            st.session_state.current_input = key
    elif key == '.' and '.' in st.session_state.current_input:
        pass # Only one decimal point allowed
    else:
        st.session_state.current_input += key


def main():
    st.set_page_config(page_title="Zhina Calculator", layout="centered")
    
    # ... (The custom CSS styling remains the same)
    st.markdown("""
        <style>
        /* General Streamlit tweaks for a calculator feel */
        .stButton>button {
            width: 100%;
            height: 70px; /* Large buttons */
            font-size: 24px;
            margin: 2px 0;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        /* Style for the display area */
        .expression-display {
            text-align: right;
            font-size: 16px;
            color: #888;
            height: 20px;
        }
        .input-display {
            text-align: right;
            font-size: 48px;
            margin-bottom: 10px;
            height: 60px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Zhina Scientific Calculator")
    
    # --- Display Area ---
    st.markdown(f'<div class="expression-display">{st.session_state.expression}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="input-display">{st.session_state.current_input}</div>', unsafe_allow_html=True)

    # Define the button layout
    r1 = ['MC', 'MR', 'M+', 'sqrt']
    r2 = ['C', '/', '*', '-'] 
    r3 = ['7', '8', '9', '+']
    r4 = ['4', '5', '6']
    r5 = ['1', '2', '3']
    r6 = ['0', '.', '=']

    # --- Button Grid ---
    
    # ... (The button layout logic is the same: R1, R2, R3, R4, R5, R6)
    for row_keys in [r1, r2, r3, r4, r5]:
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        for i, key in enumerate(row_keys):
            cols[i].button(key, key=key, on_click=handle_button, args=(key,))
            
    # Final Row (R6) - '0', '.', '='
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1]) 
    col1.button('0', key='0', on_click=handle_button, args=('0',))
    col2.button('.', key='.', on_click=handle_button, args=('.',))
    col4.button('=', key='=', on_click=handle_button, args=('=',)) 
    
    # Display Memory Status
    st.markdown("---")
    st.info(f"Memory (MR/M+): **{st.session_state.calc.memory_recall():.4f}**")

if __name__ == '__main__':
    main()
import streamlit as st
import math

# --- 1. Core Calculator Logic (Unchanged) ---

class ZhinaScientificCalculator:
    """Core mathematical logic for the Zhina Scientific Calculator."""
    # ... (All methods are the same: add, subtract, multiply, divide, power, sqrt, log, memory_add/recall/clear)
    # ... (Retaining the original methods for brevity in the re-check)
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state.memory = 0

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            st.error("Error: Cannot divide by zero.")
            return None
        return a / b

    def square_root(self, x):
        if x < 0:
            st.error("Error: Cannot take the square root of a negative number.")
            return None
        return math.sqrt(x)
    
    # ... (other scientific functions omitted for brevity in the re-check)

    def memory_add(self, value):
        st.session_state.memory += value
    def memory_recall(self):
        return st.session_state.memory
    def memory_clear(self):
        st.session_state.memory = 0
        
# --- 2. Calculation Function (Using eval() for simplicity, but acknowledge the risk) ---

def calculate(full_expression):
    """
    ATTENTION: This function uses eval() for simplicity. 
    REPLACE THIS with a safer library (like NumExpr) for production use.
    """
    # Simple string substitutions to handle basic scientific notation if needed
    full_expression = full_expression.replace('^', '**')

    try:
        # **The Vulnerable Line - Use with Caution**
        result = eval(full_expression) 
        return str(result)
    except Exception as e:
        return "Error"


# --- 3. Streamlit Application Interface (Refined) ---

# Initialize state variables
if 'current_input' not in st.session_state:
    st.session_state.current_input = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'calc' not in st.session_state:
    st.session_state.calc = ZhinaScientificCalculator()


def handle_button(key):
    """Updates the input based on the button pressed."""
    
    # --- Clear/Equals ---
    if key == 'C':
        st.session_state.current_input = '0'
        st.session_state.expression = ''
        return
    
    if key == '=':
        full_expression = st.session_state.expression + st.session_state.current_input
        result_str = calculate(full_expression)
        
        # Update display
        if result_str == "Error":
             st.session_state.expression = ''
        else:
             st.session_state.expression = full_expression + '='
        
        st.session_state.current_input = result_str
        return

    # --- Operators ---
    if key in ['+', '-', '*', '/']:
        # Append current number and operator to the expression
        st.session_state.expression += st.session_state.current_input + key
        st.session_state.current_input = '0'
        return

    # --- Memory Keys ---
    if key == 'MR':
        st.session_state.current_input = str(st.session_state.calc.memory_recall())
        return
    if key == 'M+':
        try:
            # Only add the current number input, not the whole expression result
            st.session_state.calc.memory_add(float(st.session_state.current_input))
            st.toast(f"Added {st.session_state.current_input} to Memory ({st.session_state.calc.memory_recall():.4f})")
        except ValueError:
             st.toast("Invalid value for M+")
        return
    if key == 'MC':
        st.session_state.calc.memory_clear()
        st.toast("Memory Cleared!")
        return

    # --- Scientific Functions (Directly call the method) ---
    if key == 'sqrt':
        try:
            current_value = float(st.session_state.current_input)
            result = st.session_state.calc.square_root(current_value)
            
            if result is not None:
                st.session_state.current_input = str(result)
                st.session_state.expression = f"sqrt({current_value})=" # Show function in expression
        except ValueError:
            st.session_state.current_input = "Error"
        return

    # --- Standard Keys (0-9, .) ---
    if st.session_state.current_input == '0' or st.session_state.current_input == "Error":
        # Clear '0' or 'Error' when a new digit is pressed
        if key == '.':
             st.session_state.current_input = '0.'
        else:
            st.session_state.current_input = key
    elif key == '.' and '.' in st.session_state.current_input:
        pass # Only one decimal point allowed
    else:
        st.session_state.current_input += key


def main():
    st.set_page_config(page_title="Zhina Calculator", layout="centered")
    
    # ... (The custom CSS styling remains the same)
    st.markdown("""
        <style>
        /* General Streamlit tweaks for a calculator feel */
        .stButton>button {
            width: 100%;
            height: 70px; /* Large buttons */
            font-size: 24px;
            margin: 2px 0;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        /* Style for the display area */
        .expression-display {
            text-align: right;
            font-size: 16px;
            color: #888;
            height: 20px;
        }
        .input-display {
            text-align: right;
            font-size: 48px;
            margin-bottom: 10px;
            height: 60px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Zhina Scientific Calculator")
    
    # --- Display Area ---
    st.markdown(f'<div class="expression-display">{st.session_state.expression}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="input-display">{st.session_state.current_input}</div>', unsafe_allow_html=True)

    # Define the button layout
    r1 = ['MC', 'MR', 'M+', 'sqrt']
    r2 = ['C', '/', '*', '-'] 
    r3 = ['7', '8', '9', '+']
    r4 = ['4', '5', '6']
    r5 = ['1', '2', '3']
    r6 = ['0', '.', '=']

    # --- Button Grid ---
    
    # ... (The button layout logic is the same: R1, R2, R3, R4, R5, R6)
    for row_keys in [r1, r2, r3, r4, r5]:
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        for i, key in enumerate(row_keys):
            cols[i].button(key, key=key, on_click=handle_button, args=(key,))
            
    # Final Row (R6) - '0', '.', '='
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1]) 
    col1.button('0', key='0', on_click=handle_button, args=('0',))
    col2.button('.', key='.', on_click=handle_button, args=('.',))
    col4.button('=', key='=', on_click=handle_button, args=('=',)) 
    
    # Display Memory Status
    st.markdown("---")
    st.info(f"Memory (MR/M+): **{st.session_state.calc.memory_recall():.4f}**")

if __name__ == '__main__':
    main()
import streamlit as st
import math

# --- 1. Core Calculator Logic (Unchanged) ---

class ZhinaScientificCalculator:
    """Core mathematical logic for the Zhina Scientific Calculator."""
    # ... (All methods are the same: add, subtract, multiply, divide, power, sqrt, log, memory_add/recall/clear)
    # ... (Retaining the original methods for brevity in the re-check)
    def __init__(self):
        if 'memory' not in st.session_state:
            st.session_state.memory = 0

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0:
            st.error("Error: Cannot divide by zero.")
            return None
        return a / b

    def square_root(self, x):
        if x < 0:
            st.error("Error: Cannot take the square root of a negative number.")
            return None
        return math.sqrt(x)
    
    # ... (other scientific functions omitted for brevity in the re-check)

    def memory_add(self, value):
        st.session_state.memory += value
    def memory_recall(self):
        return st.session_state.memory
    def memory_clear(self):
        st.session_state.memory = 0
        
# --- 2. Calculation Function (Using eval() for simplicity, but acknowledge the risk) ---

def calculate(full_expression):
    """
    ATTENTION: This function uses eval() for simplicity. 
    REPLACE THIS with a safer library (like NumExpr) for production use.
    """
    # Simple string substitutions to handle basic scientific notation if needed
    full_expression = full_expression.replace('^', '**')

    try:
        # **The Vulnerable Line - Use with Caution**
        result = eval(full_expression) 
        return str(result)
    except Exception as e:
        return "Error"


# --- 3. Streamlit Application Interface (Refined) ---

# Initialize state variables
if 'current_input' not in st.session_state:
    st.session_state.current_input = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'calc' not in st.session_state:
    st.session_state.calc = ZhinaScientificCalculator()


def handle_button(key):
    """Updates the input based on the button pressed."""
    
    # --- Clear/Equals ---
    if key == 'C':
        st.session_state.current_input = '0'
        st.session_state.expression = ''
        return
    
    if key == '=':
        full_expression = st.session_state.expression + st.session_state.current_input
        result_str = calculate(full_expression)
        
        # Update display
        if result_str == "Error":
             st.session_state.expression = ''
        else:
             st.session_state.expression = full_expression + '='
        
        st.session_state.current_input = result_str
        return

    # --- Operators ---
    if key in ['+', '-', '*', '/']:
        # Append current number and operator to the expression
        st.session_state.expression += st.session_state.current_input + key
        st.session_state.current_input = '0'
        return

    # --- Memory Keys ---
    if key == 'MR':
        st.session_state.current_input = str(st.session_state.calc.memory_recall())
        return
    if key == 'M+':
        try:
            # Only add the current number input, not the whole expression result
            st.session_state.calc.memory_add(float(st.session_state.current_input))
            st.toast(f"Added {st.session_state.current_input} to Memory ({st.session_state.calc.memory_recall():.4f})")
        except ValueError:
             st.toast("Invalid value for M+")
        return
    if key == 'MC':
        st.session_state.calc.memory_clear()
        st.toast("Memory Cleared!")
        return

    # --- Scientific Functions (Directly call the method) ---
    if key == 'sqrt':
        try:
            current_value = float(st.session_state.current_input)
            result = st.session_state.calc.square_root(current_value)
            
            if result is not None:
                st.session_state.current_input = str(result)
                st.session_state.expression = f"sqrt({current_value})=" # Show function in expression
        except ValueError:
            st.session_state.current_input = "Error"
        return

    # --- Standard Keys (0-9, .) ---
    if st.session_state.current_input == '0' or st.session_state.current_input == "Error":
        # Clear '0' or 'Error' when a new digit is pressed
        if key == '.':
             st.session_state.current_input = '0.'
        else:
            st.session_state.current_input = key
    elif key == '.' and '.' in st.session_state.current_input:
        pass # Only one decimal point allowed
    else:
        st.session_state.current_input += key


def main():
    st.set_page_config(page_title="Zhina Calculator", layout="centered")
    
    # ... (The custom CSS styling remains the same)
    st.markdown("""
        <style>
        /* General Streamlit tweaks for a calculator feel */
        .stButton>button {
            width: 100%;
            height: 70px; /* Large buttons */
            font-size: 24px;
            margin: 2px 0;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        /* Style for the display area */
        .expression-display {
            text-align: right;
            font-size: 16px;
            color: #888;
            height: 20px;
        }
        .input-display {
            text-align: right;
            font-size: 48px;
            margin-bottom: 10px;
            height: 60px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Zhina Scientific Calculator")
    
    # --- Display Area ---
    st.markdown(f'<div class="expression-display">{st.session_state.expression}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="input-display">{st.session_state.current_input}</div>', unsafe_allow_html=True)

    # Define the button layout
    r1 = ['MC', 'MR', 'M+', 'sqrt']
    r2 = ['C', '/', '*', '-'] 
    r3 = ['7', '8', '9', '+']
    r4 = ['4', '5', '6']
    r5 = ['1', '2', '3']
    r6 = ['0', '.', '=']

    # --- Button Grid ---
    
    # ... (The button layout logic is the same: R1, R2, R3, R4, R5, R6)
    for row_keys in [r1, r2, r3, r4, r5]:
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        for i, key in enumerate(row_keys):
            cols[i].button(key, key=key, on_click=handle_button, args=(key,))
            
    # Final Row (R6) - '0', '.', '='
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1]) 
    col1.button('0', key='0', on_click=handle_button, args=('0',))
    col2.button('.', key='.', on_click=handle_button, args=('.',))
    col4.button('=', key='=', on_click=handle_button, args=('=',)) 
    
    # Display Memory Status
    st.markdown("---")
    st.info(f"Memory (MR/M+): **{st.session_state.calc.memory_recall():.4f}**")

if __name__ == '__main__':
    main()
    col2.button('.', key='.', on_click=handle_button, args=('.',))
    col4.button('=', key='=', on_click=handle_button, args=('=',)) 
    
    # Display Memory Status
    st.markdown("---")
    st.info(f"Memory (MR/M+): **{st.session_state.calc.memory_recall():.4f}**")

if __name__ == '__main__':
    main()

