"""Pitaka Laxmi Venkata Naga Satya (2203124)
   Banoth Anusha (2203104)
"""
import tkinter as tk
from tkinter import messagebox, ttk
from sympy import symbols, Poly
from sympy.abc import x
import random

# Constants for styling
FONT = ("Arial", 12)
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4CAF50"
TEXT_COLOR = "#333333"
ERROR_COLOR = "#FF0000"

def find_generator_polynomial(n, k):
    """
    Find the generator polynomial g(x) for a cyclic code with parameters n and k.
    The generator polynomial is the minimal polynomial of the form x^r + ... + 1,
    where r = n - k.
    """
    r = n - k
    # Generating all possible polynomials of degree r over F2
    # and finding the one that divides x^n - 1
    x_poly = Poly(x**n - 1, domain='GF(2)')
    for i in range(1, 2**(r + 1)):  # Starting from 1 to avoid zero polynomial
        coeffs = [int(bit) for bit in f"{i:0{r+1}b}"]
        g_poly = Poly(coeffs, x, domain='GF(2)')
        if g_poly.degree() == r and x_poly % g_poly == 0:
            return g_poly
    return None

def encode_message(message, g_poly, n, k):
    """
    Encode a message using the generator polynomial g(x).
    The message is a binary string of length k.
    """
    # Converting message to polynomial
    m_poly = Poly([int(bit) for bit in message], x, domain='GF(2)')
    # Multiplying by x^(n-k) to shift the message
    shifted_poly = m_poly * Poly(x**(n-k), domain='GF(2)')
    # Computing remainder to get parity bits
    remainder = shifted_poly % g_poly
    # Combining to form codeword
    codeword_poly = shifted_poly + remainder
    # Converting to binary string
    codeword = ''.join(str(int(coeff)) for coeff in codeword_poly.all_coeffs())
    return codeword.zfill(n)

def on_encode():
    try:
        n = int(entry_n.get())
        k = int(entry_k.get())

        if n <= k:
            messagebox.showerror("Error", "n must be greater than k.")
            return

        # Checking if the user wants to generate the message automatically
        if message_option.get() == "auto":
            # Generating a random binary message of length k
            message = ''.join(random.choice('01') for _ in range(k))
            entry_message.delete(0, tk.END)
            entry_message.insert(0, message)
        else:
            # Getting the message from the entry field
            message = entry_message.get()
            if len(message) != k:
                messagebox.showerror("Error", f"Message must be exactly {k} bits long.")
                return

        # Finding generator polynomial
        g_poly = find_generator_polynomial(n, k)
        if g_poly is None:
            messagebox.showerror("Error", f"No valid generator polynomial exists for n={n} and k={k}.")
            return

        # Encoding the message
        codeword = encode_message(message, g_poly, n, k)

        # Displaying results
        label_g_poly.config(text=f"Generator Polynomial: {g_poly.as_expr()}")
        label_codeword.config(text=f"Encoded Codeword: {codeword}")

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter integers for n and k.")

# GUI Setup
root = tk.Tk()
root.title("Cyclic Code Encoder")
root.geometry("500x400")
root.configure(bg=BG_COLOR)

# Styling
style = ttk.Style()
style.configure("TButton", font=FONT, background=BUTTON_COLOR, foreground=TEXT_COLOR)
style.configure("TLabel", font=FONT, background=BG_COLOR, foreground=TEXT_COLOR)
style.configure("TRadiobutton", font=FONT, background=BG_COLOR, foreground=TEXT_COLOR)

# Input fields
label_n = ttk.Label(root, text="n (codeword length):")
label_n.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_n = ttk.Entry(root, font=FONT)
entry_n.grid(row=0, column=1, padx=10, pady=10)

label_k = ttk.Label(root, text="k (message length):")
label_k.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_k = ttk.Entry(root, font=FONT)
entry_k.grid(row=1, column=1, padx=10, pady=10)

# Message input option
message_option = tk.StringVar(value="manual")  # Default to manual input
label_option = ttk.Label(root, text="Message Input Option:")
label_option.grid(row=2, column=0, padx=10, pady=10, sticky="w")
radio_manual = ttk.Radiobutton(root, text="Manual", variable=message_option, value="manual")
radio_manual.grid(row=2, column=1, padx=10, pady=5, sticky="w")
radio_auto = ttk.Radiobutton(root, text="Auto Generate", variable=message_option, value="auto")
radio_auto.grid(row=3, column=1, padx=10, pady=5, sticky="w")

label_message = ttk.Label(root, text="Message (k bits):")
label_message.grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_message = ttk.Entry(root, font=FONT)
entry_message.grid(row=4, column=1, padx=10, pady=10)

# Encoding button
button_encode = ttk.Button(root, text="Encode", command=on_encode)
button_encode.grid(row=5, column=0, columnspan=2, pady=20)

# Output fields
label_g_poly = ttk.Label(root, text="Generator Polynomial: ", font=FONT)
label_g_poly.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

label_codeword = ttk.Label(root, text="Encoded Codeword: ", font=FONT)
label_codeword.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Running the GUI
root.mainloop()