import tkinter as tk
import math

# Function to update the expression when a button is pressed
def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)  # Clear the current input
    entry.insert(tk.END, current + value)  # Add the new input to the existing input

# Function to evaluate the expression
def button_equal():
    try:
        result = eval(entry.get())  # Evaluate the expression in the entry
        entry.delete(0, tk.END)  # Clear the entry
        entry.insert(tk.END, result)  # Display the result
    except Exception as e:
        entry.delete(0, tk.END)  # Clear the entry
        entry.insert(tk.END, "Error")  # Display error if there's an issue with evaluation

# Function to clear the entry
def button_clear():
    entry.delete(0, tk.END)

# Function to handle backspace
def button_backspace():
    current = entry.get()
    entry.delete(len(current)-1, tk.END)  # Delete the last character

# Create the main window
root = tk.Tk()
root.title("Casio FX-82AU Plus 2")

# Create the entry widget to display the input/output
entry = tk.Entry(root, width=20, font=("Arial", 18), borderwidth=2, relief="solid", justify="right")
entry.grid(row=0, column=0, columnspan=4)

# Define the buttons for the calculator (basic operations, trigonometry, log, etc.)
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log', 5, 3),
    ('sqrt', 6, 0), ('(', 6, 1), (')', 6, 2), ('C', 6, 3),
    ('Backspace', 7, 0, 4)  # Button for backspace (combined across multiple columns)
]

# Create and place buttons on the grid
for (text, row, col, *span) in buttons:
    if text == '=':
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=button_equal)
    elif text == 'C':
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=button_clear)
    elif text == 'Backspace':
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=button_backspace)
        button.grid(row=row, column=col, columnspan=4, sticky="nsew")
        continue
    else:
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=lambda t=text: button_click(t))
    
    button.grid(row=row, column=col, sticky="nsew")

# Define button functions for scientific operations (sin, cos, tan, sqrt, log)
def scientific_function(func):
    try:
        expression = entry.get()
        if func == 'sin':
            result = math.sin(math.radians(float(expression)))  # Convert to radians for trigonometric functions
        elif func == 'cos':
            result = math.cos(math.radians(float(expression)))
        elif func == 'tan':
            result = math.tan(math.radians(float(expression)))
        elif func == 'sqrt':
            result = math.sqrt(float(expression))
        elif func == 'log':
            result = math.log(float(expression))
        
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Attach scientific functions to buttons
def attach_scientific_buttons():
    for text in ['sin', 'cos', 'tan', 'sqrt', 'log']:
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=lambda t=text: scientific_function(t))
        button.grid(row=5, column=buttons.index((text, 5, 0)), sticky="nsew")

# Run the main loop
root.mainloop()
