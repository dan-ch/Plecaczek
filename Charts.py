import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def charts(chart_all_iters, chart_this_iter, chart_results):
    data1 = {'Numer przedmiotu': list(range(1, len(chart_this_iter) + 1)),
             'Aktualna iteracja': chart_this_iter
             }
    df1 = DataFrame(data1, columns=['Numer przedmiotu', 'Aktualna iteracja'])

    data2 = {'Numer przedmiotu': list(range(1, len(chart_all_iters) + 1)),
             'Wszystkie iteracje': chart_all_iters
             }
    df2 = DataFrame(data2, columns=['Numer przedmiotu', 'Wszystkie iteracje'])

    data3 = {'Iteracja': list(map(lambda res_iter: res_iter.iteration, chart_results)),
            'Wynik': list(map(lambda result: result.value, chart_results))
             }
    df3 = DataFrame(data3, columns=['Iteracja', 'Wynik'])

    root = tk.Tk()

    figure1 = plt.Figure(figsize=(6, 5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df1 = df1[['Numer przedmiotu', 'Aktualna iteracja']].groupby('Numer przedmiotu').sum()
    df1.plot(kind='bar', legend=False, ax=ax1, color='b')
    ax1.set_title('Najczęściej wybierany przedmiot w danej iteracji')


    figure2 = plt.Figure(figsize=(6, 5), dpi=100)
    ax2 = figure2.add_subplot(111)
    bar2 = FigureCanvasTkAgg(figure2, root)
    bar2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df2 = df2[['Numer przedmiotu', 'Wszystkie iteracje']].groupby('Numer przedmiotu').sum()
    df2.plot(kind='bar', legend=False, color='c', ax=ax2)
    ax2.set_title('Najczęściej wybierany przedmiot we wszystkich iteracjach')

    figure3 = plt.Figure(figsize=(6, 5), dpi=100)
    ax3 = figure3.add_subplot(111)
    line3 = FigureCanvasTkAgg(figure3, root)
    line3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df3 = df3[['Iteracja', 'Wynik']].groupby('Iteracja').sum()
    df3.plot(kind='line', legend=False, ax=ax3, color='m', marker='o', fontsize=10)
    ax3.set_title('Zależność wyniku od iteracji')

    root.mainloop()
