#!/usr/bin/env python3
"""
TEST GUI - Ultra simple to test visibility
"""

import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("TEST - Can you see the yellow box?")
root.geometry("600x500")
root.configure(bg='white')

# Title
label = tk.Label(root, text="If you see this text, labels work!", 
                font=("Arial", 16), bg='white', fg='blue')
label.pack(pady=20)

# TEST: Scrolled Text Widget (should be more visible)
test_text = scrolledtext.ScrolledText(
    root,
    font=("Arial", 16),
    height=15,
    width=40,
    bg='yellow',
    fg='black',
    relief=tk.SOLID,
    borderwidth=5
)
test_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
test_text.insert("1.0", "HELLO! Can you see this big yellow box with black text?\n\nType here to test!")

# Button
btn = tk.Button(root, text="I CAN SEE THE YELLOW BOX!", 
               font=("Arial", 14), bg='green', fg='white', padx=20, pady=10)
btn.pack(pady=10)

root.mainloop()

