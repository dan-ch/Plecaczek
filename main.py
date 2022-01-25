import csv
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

import Charts
import ClonAlg
import Item
from Point import Point
from Item import Item

min_value, max_value = (0.5, 25)
min_weight, max_weight = (1.0, 30)
knapsack_capacity = 50
number_of_items = 10
number_of_choices = 5
number_of_clones = 10
mutation_rate = 0.5
succession = 'elitarna'
iteration = 0
elapsed_time = 0
alg_elapsed_time = 0
chart_all_iters = []
chart_this_iter = []
chart_results = []


items: tuple[Item] = tuple()
items_choices = []

# GUI

root = tk.Tk()

root.title('Algorithm')
root.geometry("830x950")


def clear_list(list_box):
    for i in list_box.get_children():
        list_box.delete(i)


def fetch_data_to_table(choices):
    for i, choice in enumerate(choices):
        listBox.insert('', tk.END, values=(i, choice.weight, choice.totalValue, choice.affinity))


def run(from_file: bool):
    clear_list(tree_view)
    global items, items_choices, number_of_items, min_weight, max_weight, min_value, max_value, number_of_choices, \
        knapsack_capacity, number_of_clones, mutation_rate, iteration, succession, alg_elapsed_time, iteration,\
        chart_all_iters, chart_this_iter, chart_results
    iteration = 0
    min_value = MinValue.get()
    max_value = MaxValue.get()
    min_weight = MinWeight.get()
    max_weight = MaxWeight.get()
    knapsack_capacity = KnapsackCapacity.get()
    number_of_choices = NumberOfChoices.get()
    number_of_clones = NumberOfClones.get()
    mutation_rate = MutationRate.get()
    succession = Succession.get()
    if from_file:
        get_data_from_file()
    else:
        number_of_items = NumberOfItems.get()
        items = ClonAlg.create_random_items(number_of_items, min_weight, max_weight, min_value, max_value)
    items_choices = ClonAlg.create_random_choices(number_of_choices, items, knapsack_capacity)
    clear_list(listBox)
    fetch_data_to_table(items_choices)
    alg_elapsed_time = 0
    iteration = 0
    alg_elapsed_time_lbl.config(text=alg_elapsed_time)
    lbl_iter.config(text=iteration)
    chart_all_iters = [0] * number_of_items
    chart_this_iter = [0] * number_of_items
    chart_results = []
    print(chart_all_iters)
    print(chart_this_iter)


#nowe
def count_all_items_choices():
    global chart_all_iters, items_choices, number_of_items
    for choice in items_choices:
        for i in range(number_of_items):
            chart_all_iters[i] += choice.binary_array[i]


def count_this_iter_choices():
    global items_choices, number_of_items, chart_this_iter
    chart_this_iter = [0] * number_of_items
    for choice in items_choices:
        for i in range(number_of_items):
            chart_this_iter[i] += choice.binary_array[i]



def step(steps: int):
    clear_list(listBox)
    temp_elapsed_time = 0

    global items, items_choices, mutation_rate, knapsack_capacity, number_of_choices, number_of_clones, succession, iteration, alg_elapsed_time
    start = time.time()
    for i in range(steps):
        items_choices = ClonAlg.make_step(items_choices, items, knapsack_capacity, number_of_choices, number_of_clones,
                                          mutation_rate, succession)
        count_all_items_choices()
    count_this_iter_choices()
    end = time.time()
    temp_elapsed_time = end - start
    alg_elapsed_time += temp_elapsed_time
    iteration += steps
    fetch_data_to_table(items_choices)
    lbl_iter.config(text=iteration)
    alg_elapsed_time_lbl.config(text=alg_elapsed_time)
    main_chart()
    chart_results.append(Point(iteration, items_choices[1].totalValue))


def get_data_from_file():
    global items, number_of_items
    new_items = []
    with open('items.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            item = Item(float(row[0]), float(row[1]))
            new_items.append(item)
            line_count += 1
        print(f'Processed {line_count} item lines.')
    items = tuple(new_items)
    number_of_items = line_count


def go_bruteforce():
    global elapsed_time
    elapsed_time, brute_force_choice = ClonAlg.bruteForce(number_of_items, knapsack_capacity, items)
    tree_view.insert('', tk.END,
                     values=(brute_force_choice.weight, brute_force_choice.totalValue, brute_force_choice.binary_array))
    brt_el_time.config(text=elapsed_time)

succession_list = ['elitarna', 'losowa', 'scisk']

# WYŚWIETLANIE KONTROLEK
tk.Label(root, text="Min waga przedmiotu").grid(row=0, column=0)
MinWeight = tk.DoubleVar(name="MinWeight")
tk.Spinbox(root, increment=0.01, from_=0.1, to=25, textvariable=MinWeight).grid(row=1, column=0)
tk.Label(root, text="Max waga przedmiotu").grid(row=2, column=0)
MaxWeight = tk.DoubleVar(name="MaxWeight")
tk.Spinbox(root, increment=0.01, from_=25, to=50, textvariable=MaxWeight).grid(row=3, column=0)

tk.Label(root, text="Min wartość przedmiotu").grid(row=0, column=1)
MinValue = tk.DoubleVar(name="MinValue")
tk.Spinbox(root, increment=0.01, from_=1, to=50, textvariable=MinValue).grid(row=1, column=1)
tk.Label(root, text="Max wartość przedmiotu").grid(row=2, column=1)
MaxValue = tk.DoubleVar(name="MaxValue")
tk.Spinbox(root, increment=0.01, from_=50, to=100, textvariable=MaxValue).grid(row=3, column=1)

tk.Label(root, text="Ilość klonów").grid(row=0, column=2)
NumberOfClones = tk.IntVar(name="NumberOfClones")
tk.Spinbox(root, increment=5, from_=10, to=100, textvariable=NumberOfClones).grid(row=1, column=2)
tk.Label(root, text="Ilośc przedmiotów").grid(row=2, column=2)
NumberOfItems = tk.IntVar(name="NumberOfItems")
tk.Spinbox(root, increment=10, from_=10, to=100, textvariable=NumberOfItems).grid(row=3, column=2)

tk.Label(root, text="Ilość wyborów").grid(row=0, column=3)
NumberOfChoices = tk.IntVar(name="NumberOfChoices")
tk.Spinbox(root, increment=1, from_=5, to=25, textvariable=NumberOfChoices).grid(row=1, column=3)
tk.Label(root, text="Rozmiar plecaka").grid(row=2, column=3)
KnapsackCapacity = tk.IntVar(name="KnapsackCapacity")
tk.Spinbox(root, increment=10, from_=50, to=200, textvariable=KnapsackCapacity).grid(row=3, column=3)

tk.Label(root, text="P. mutacji").grid(row=0, column=4)
MutationRate = tk.DoubleVar(name="MutationRate")
tk.Spinbox(root, increment=0.05, from_=0.1, to=0.9, textvariable=MutationRate).grid(row=1, column=4)
tk.Label(root, text="Sukcesja").grid(row=2, column=4)
Succession = tk.StringVar(name="Succession")
Succession.set(succession_list[0])
dropdown = OptionMenu(
    root,
    Succession,
    *succession_list,
)
dropdown.grid(row=3, column=4)
tk.Label(root, text="Iteracje:").grid(row=0, column=5)
lbl_iter = tk.Label(root, text="0")
lbl_iter.grid(row=1, column=5)
tk.Button(root, text="START", width=15, command=lambda: run(False), bg='#ffb3fe').grid(row=3, column=5)

tk.Button(root, text="Next 10 step ", width=15, command=lambda: step(10), bg="#88fc03").grid(row=4, column=0)
tk.Button(root, text="Next 100 steps", width=15, command=lambda: step(100), bg="#88fc03").grid(row=4, column=1)
tk.Button(root, text="Close", width=15, command=exit, bg='#fc033d').grid(row=4, column=2)
tk.Button(root, text="Bruteforce", width=15, command=go_bruteforce, bg='#fc033d').grid(row=4, column=3)
tk.Button(root, text="Wczytaj csv", command=lambda: run(True), bg='#ac47ff').grid(row=4, column=4)
tk.Button(root, text="Wykresy", command=lambda: Charts.charts(chart_all_iters, chart_this_iter, chart_results), bg='#ff9a47').grid(row=4, column=5)
# tk.Button(root, text="Show results", width=15, command=showResults, bg='#036bfc').grid(row=4, column=3)

tk.Label(root, text="Lista wyborów", font=("Arial", 20)).grid(row=6, columnspan=6)
cols = ('Position', 'Weight', 'Value', 'Affinity')

listBox = ttk.Treeview(root, columns=cols, show='headings', height=5)
for col in cols:
    listBox.heading(col, text=col)
listBox.grid(row=7, column=0, columnspan=6)

tk.Label(root, text="Czas wykonywania algorytmu").grid(row=8, column=2)
alg_elapsed_time_lbl = tk.Label(root, text='0')
alg_elapsed_time_lbl.grid(row=8, column=3)

tk.Label(root, text="Wynik z bruteforce", font=("Arial", 20)).grid(row=9, columnspan=6)
bruteForceColumns = ('Weight', 'Value', 'Binary array')
tree_view = ttk.Treeview(root, columns=bruteForceColumns, show='headings', height=1)
for column in bruteForceColumns:
    tree_view.heading(column, text=column)
tree_view.column('Binary array', width=400)
tree_view.grid(row=10, column=0, columnspan=6)
tk.Label(root, text="Czas wykonywania algorytmu: ").grid(row=11, column=2)
brt_el_time = tk.Label(root, text=elapsed_time)
brt_el_time.grid(row=11, column=3)

def find_max_index(number_list):
    max_value = max(number_list)
    max_index = number_list.index(max_value)
    return max_index

def main_chart():
    global chart_all_iters
    explodeTuple = [0.03] * len(chart_all_iters)
    explodeTuple[find_max_index(chart_all_iters)] = 0.12
    df2 = DataFrame({'Numer przedmiotu': chart_all_iters},
                    index = list(range(1, len(chart_all_iters) + 1)))

    figure2 = plt.Figure(figsize=(5, 5), dpi=100)
    ax2 = figure2.add_subplot(111)
    bar2 = FigureCanvasTkAgg(figure2, root)
    bar2.get_tk_widget().grid(row=12, column=0, columnspan=6)
    ax2.set_title('Najczęściej wybierany przedmiot we wszystkich iteracjach')
    pie_plot = df2.plot.pie(y='Numer przedmiotu', figsize=(5, 5), ax=ax2, legend=False, autopct='%1.1f%%',
                            explode=explodeTuple)

root.mainloop()

