import itertools
import random
import time

from numpy.random import uniform

from Choice import Choice
from Item import Item

total_affinity = 0.0


def create_random_items(number_of_items: int, min_weight: float, max_weight: float, min_value: float, max_value: float):
    items = tuple(
        [Item(uniform(min_weight, max_weight), uniform(min_value, max_value)) for x in range(number_of_items)])
    return items


def create_random_choices(number_of_choices: int, items: tuple[Item], knapsack_capacity: int):
    choices = []
    for j in range(number_of_choices):
        choice = Choice()
        for i in range(len(items)):
            choose = random.randint(0, 1)
            choice.binary_array.append(choose)
        choices.append(choice)
    calculate_weight_totalValue(choices, items)
    reduce_weight(choices, items, knapsack_capacity)
    calculate_affinity(choices, knapsack_capacity)
    count_total_affinity(choices)
    return choices


def count_total_affinity(choices: [Choice]):
    global total_affinity
    total_affinity = 0
    for choice in choices:
        total_affinity += choice.affinity


def elite_succession(choices: [Choice], number_of_choices: int):
    sorted_choices = sorted(choices, key=lambda choice: choice.totalValue, reverse=True)
    return sorted_choices[:number_of_choices]


# nowe
def random_succession(choices: [Choice], number_of_choices: int):
    return random.sample(choices, number_of_choices)


# nowe
def crush_succession(choices: [Choice], number_of_choices: int):
    index = 0
    diff = float('inf')
    choices = sorted(choices, key=lambda choice: choice.totalValue, reverse=True)
    while len(choices) > number_of_choices:
        for i in range(0, len(choices) - 1):
            if abs(choices[i].totalValue - choices[i + 1].totalValue) < diff:
                diff = abs(choices[i].totalValue - choices[i + 1].totalValue)
                index = i
        diff = float('inf')
        del choices[index]
    return choices


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
    for choice in choices:
        choice.weight = 0
        choice.totalValue = 0
        for i in range(len(choice.binary_array)):
            if choice.binary_array[i] == 1:
                choice.totalValue += items[i].value
                choice.weight += items[i].weight
    return choices


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
    tmp_item = []
    for item in choice.binary_array:
        if uniform(0, 1) < mutation_rate:
            tmp_item.append(1) if item == 0 else tmp_item.append(0)
        else:
            tmp_item.append(item)
    choice.binary_array = tmp_item
    return choice


def make_step(item_choices: [Choice], items: tuple[Item], knapsack_capacity: int, number_of_choices: int,
              number_of_clones: int, mutation_rate: float, succession: str):
    count_total_affinity(item_choices)
    new_population = item_choices
    clone_choices = []
    after_succession = []

    for choice in item_choices:
        clone_choices = clone(choice, number_of_clones)
    for clone_choice in clone_choices:
        new_population.append(mutate(clone_choice, mutation_rate))
    calculate_weight_totalValue(new_population, items)
    reduce_weight(new_population, items, knapsack_capacity)
    calculate_affinity(new_population, knapsack_capacity)
    match succession:
        case "elitarna":
            after_succession = elite_succession(new_population, number_of_choices)
        case "losowa":
            after_succession = random_succession(new_population, number_of_choices)
        case "scisk":
            after_succession = crush_succession(new_population, number_of_choices)
    return after_succession


# nowe
def bruteForce(number_of_items: int, knapsack_capacity: int, items: tuple[Item]):
    start = time.time()
    allBinaryCombinations = list(itertools.product([0, 1], repeat=number_of_items))
    list_of_choices = []
    choices_fits_knapsack = []

    for combination in allBinaryCombinations:
        choice = Choice()
        choice.binary_array = list(combination)
        list_of_choices.append(choice)
    calculate_weight_totalValue(list_of_choices, items)

    for choice in list_of_choices:
        if choice.weight <= knapsack_capacity:
            choices_fits_knapsack.append(choice)

    sorted_choices = sorted(choices_fits_knapsack, key=lambda choice: choice.totalValue, reverse=True)
    end = time.time()
    elapsed_time = end - start
    return elapsed_time, sorted_choices[0]

# TODO wykresy
