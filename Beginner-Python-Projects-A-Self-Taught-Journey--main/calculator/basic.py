import tkinter as tk

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

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")

# Create the entry widget to display the input/output
entry = tk.Entry(root, width=16, font=("Arial", 24), borderwidth=2, relief="solid", justify="right")
entry.grid(row=0, column=0, columnspan=4)

# Define the buttons
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

# Create and place buttons on the grid
for (text, row, col) in buttons:
    if text == '=':
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=button_equal)
    elif text == 'C':
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=button_clear)
    else:
        button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=lambda t=text: button_click(t))
    
    button.grid(row=row, column=col)

# Run the main loop
root.mainloop()
