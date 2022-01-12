import numpy as np
import ClonAlg
import tkinter as tk
from tkinter import ttk
# import matplotlib.pyplot as plt

min_value, max_value = (0.5, 25)
min_weight, max_weight = (1.0, 30)
knapsack_capacity = 50
number_of_items = 10
number_of_choices = 5
number_of_clones = 20
mutation_rate = 0.2

max_iteration = 10
iteration = 0

items = ClonAlg.create_random_items(number_of_items, min_weight, max_weight, min_value, max_value)
items_choices = ClonAlg.create_random_choices(number_of_items, number_of_choices, items, knapsack_capacity)
items_after_step = ClonAlg.make_step(items_choices, items, knapsack_capacity, number_of_choices, number_of_clones,
                                     mutation_rate)




def show():
    for i, (weight, value) in enumerate(items_after_step, start=1):
        listBox.insert("", "end", values=(i, weight, value))

root = tk.Tk()
root.title('Algorithm')
root.geometry("800x600")
label = tk.Label(root, text="List of choices", font=("Arial", 30)).grid(row=0, columnspan=3)

# create Treeview with 3 columns
cols = ('Position', 'Weight', 'Value')
listBox = ttk.Treeview(root, columns=cols, show='headings')
# set column headings
for col in cols:
    listBox.heading(col, text=col)
listBox.grid(row=1, column=0, columnspan=2)
e1 = tk.Entry(root)
e1.grid(row=1, column=1)
tk.Button(root, text="Show new choices", width=15, command=show).grid(row=4, column=0)
tk.Button(root, text="Close", width=15, command=exit).grid(row=4, column=1)

root.mainloop()

