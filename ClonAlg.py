import random

import numpy as np
from numpy.random import uniform

from Choice import Choice
from Item import Item

total_affinity = 0.0


def create_random_items(number_of_items: int, min_weight: float, max_weight: float, min_value: float, max_value: float):
    items = tuple(
        [Item(uniform(min_weight, max_weight), uniform(min_value, max_value)) for x in range(number_of_items)])
    return items


def create_random_choices(number_of_items: int, number_of_choices: int, items: tuple[Item], knapsack_capacity: int):
    choices = []
    for j in range(number_of_choices):
        choice = Choice()
        for i in range(number_of_items):
            choose = random.randint(0, 1)
            choice.binary_array.append(choose)
        choices.append(choice)
    calculate_weight_totalValue(choices, items)
    calculate_affinity(choices, knapsack_capacity)
    count_total_affinity(choices)
    return reduce_weight(choices, items, knapsack_capacity)


# nowe
def count_total_affinity(choices: [Choice]):
    global total_affinity
    for choice in choices:
        total_affinity += choice.affinity


# nowe
def elite_succession(choices: [Choice], number_of_choices: int):
    sorted_choices = sorted(choices, key=lambda choice: choice.affinity, reverse=True)
    return sorted_choices[:number_of_choices]


def reduce_weight(choices: [Choice], items: tuple[Item], knapsack_capacity: int):
    for choice in choices:
        while choice.weight > knapsack_capacity:
            random_select = random.choice(range(0, len(choice.binary_array)))
            item = choice.binary_array[random_select]
            if item == 1:
                choice.binary_array[random_select] = 0
                choice.weight -= items[random_select].weight
                choice.totalValue -= items[random_select].value
    return choices


def calculate_weight_totalValue(choices: [Choice], items: tuple[Item]):
    tmp = []
    for choice in choices:
        choice.weight = 0
        choice.totalValue = 0
        for i in range(len(choice.binary_array)):
            if choice.binary_array[i] == 1:
                choice.totalValue += items[i].value
                choice.weight += items[i].weight
        tmp.append(choice)
    return tmp


def calculate_affinity(item_choices: [Choice], knapsack_capacity: int):
    for choice in item_choices:
        choice.affinity = choice.totalValue / knapsack_capacity  # zmiana
    return item_choices


def clone(choice: Choice, number_of_clones: int):
    clone_num = round(choice.affinity * number_of_clones / total_affinity)  # zmiana
    clones = []
    for i in range(clone_num):
        clone = Choice()
        clone.binary_array = choice.binary_array
        clones.append(clone)
    return clones


def mutate(choice: Choice, mutation_rate: float):
    if uniform(0, 1) < mutation_rate:
        tmp_item = []
        for item in choice.binary_array:
            if uniform(0, 1) < mutation_rate:
                tmp_item.append(1) if item == 0 else tmp_item.append(0)
            else:
                tmp_item.append(item)
        choice.binary_array = tmp_item
    return choice


def make_step(item_choices: [Choice], items: tuple[Item], knapsack_capacity: int, number_of_choices: int,
              number_of_clones: int, mutation_rate: float):
    new_population = item_choices
    for choice in item_choices:
        clone_choices = clone(choice, number_of_clones)
        for clone_choice in clone_choices:
            new_population.append(mutate(clone_choice, mutation_rate))
    calculate_weight_totalValue(new_population, items)
    reduce_weight(new_population, items, knapsack_capacity)
    calculate_affinity(new_population, knapsack_capacity)
    after_elite_succession = elite_succession(new_population, number_of_choices)
    return after_elite_succession
