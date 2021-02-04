import itertools
import random
from copy import deepcopy

selection_types = {1: 'турнірна селекція',
                   2: 'пропорційна (рулеткова) селекція',
                   3: 'метод ранжування'
                   }

mutation_types = {1: 'на парних ітераціях змінюємо випадковий ген на протилежний',
                  2: 'на непарних ітераціях змінюємо випадковий ген на протилежний',
                  3: 'на всіх ітераціях змінюємо випадковий ген на протилежний',
                  4: 'мутація не відбувається'}

#                                       CONFIG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
p = 24

values  = [5, 6, 8, 6, 4, 1, 3, 4, 5, 2, 1, 3, 4, 5, 2]
weights = [2, 4, 5, 4, 2, 1, 1, 2, 4, 1, 1, 2, 2, 3, 2]

s1 = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1]
s2 = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1]
s3 = [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0]
s4 = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
s5 = [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0]

start_population = [s1, s2, s3, s4, s5]

iterations = 4

selection_type = 2
rank_index = (1, 5)  # індекси осіб, що ввійдуть до селекції методу ранжування (№3).1-найкращий, 5-найгірший, 0-раптовий

crossover_points = [5, 8]
mutation_type = 2
#                                       CONFIG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


iteration = 1
start_name_index = ['S'+str(i+1) for i in range(len(start_population))]


def print_info():
    print("Місткість рюкзака:", p)

    for i in range(len(values)):
        print('{:^3}'.format(i + 1), end=' ')
    print('Номер предмета')
    for i in range(len(values)):
        print('{:^3}'.format(values[i]), end=' ')
    print("Вартість")
    for i in range(len(values)):
        print('{:^3}'.format(weights[i]), end=' ')
    print("Вага")

    print("Початкова популяція")
    for i in range(len(start_population)):
        print(start_name_index[i], start_population[i],
              "F =", ' + '.join([str(values[i]) for j in range(len(start_population[i])) if start_population[i][j] == 1]), "=", fitness(start_population[i]))

    print("Вибір батьків —", selection_types[selection_type], end='')
    if selection_type == 3:
        if rank_index == (0, 0):
            print(", обираємо дві раптових особи")
        elif rank_index[0] == 0:
            print(", обираємо", rank_index[1], "за цінністю та випадкову особу")
        elif rank_index[1] == 0:
            print(", обираємо", rank_index[0], "за цінністю та випадкову особу")
        else:
            print(", обираємо", rank_index[0], "та", rank_index[1], "за цінністю осіб")
    else:
        print()
    print("Оператор схрещування", len(crossover_points), "-точковий:", str(crossover_points)[1:-1], "включно")
    print("Оператор мутації:", mutation_types[mutation_type])


def lindexsplit(some_list, *args):
    args = (0,) + tuple(data for data in args) + (len(some_list) + 1,)
    return [some_list[start:end] for start, end in zip(args, args[1:])]


def transposed_cartesian(a, b):
    transposed = [list(i) for i in zip(*(a, b))]
    cartesian = list(itertools.product(*transposed))
    for i in range(len(cartesian)):
        cartesian[i] = list(cartesian[i])
    return cartesian


def fitness(individual):
    value, weight = 0, 0
    for i in range(len(individual)):
        if individual[i] == 1:
            value += values[i]
            weight += weights[i]
    if weight > p:
        return -1
    else:
        return value


def tournament_select(population):
    half_population1 = random.sample(population, int(len(population)/2))
    half_population2 = []
    for elem in population:
        if elem not in half_population1:
            half_population2.append(elem)

    print("Розділимо популяцію на 2 частини")
    print("Перша частина:")
    for elem in half_population1:
        print(elem, "F =", fitness(elem))
    print("Друга частина:")
    for elem in half_population2:
        print(elem, "F =", fitness(elem))
    print("Обираємо кращого з кожної частини")

    half_population1 = sorted(half_population1, key=lambda x: fitness(x), reverse=True)
    half_population2 = sorted(half_population2, key=lambda x: fitness(x), reverse=True)
    parent1, parent2 = half_population1[0], half_population2[0]
    return parent1, parent2


def roulette_select(population, name_index):
    population = sorted(population, key=lambda x: fitness(x), reverse=True)
    probabilities = [fitness(x) for x in population]
    parent1, parent2 = None, None

    print("Обираємо батьків, шанси кожного прямо пропорційні F, обернено пропорційні сумарному F популяції")
    sum_f = sum([fitness(population[i]) for i in range(len(population))])
    print("Sum(f)=", sum_f)
    for i in range(len(population)):
        print("Шанс", name_index[i], "--", fitness(population[i]), '/', sum_f)
    while parent1 == parent2:
        parents = (random.choices(population, probabilities, k=2))
        parent1, parent2 = parents[0], parents[1]
    return parent1, parent2


def ranked_select(population):
    population = sorted(population, key=lambda x: fitness(x), reverse=True)
    if rank_index == (0, 0):
        print("Обираємо 2 довільних елементи")
        parents = random.sample(population, 2)
        parent1, parent2 = parents[0], parents[1]
    elif rank_index[0] == 0:
        print("Обираємо", rank_index[1], "за цінністю та випадкову особу")
        parent1 = random.choice(population)
        parent2 = population[rank_index[1] - 1]
        if parent1 == parent2 and population.count(parent1) == 1:
            while parent1 == parent2:
                parent1 = random.choice(population)
    elif rank_index[1] == 0:
        print("Обираємо", rank_index[0], "за цінністю та випадкову особу")
        parent2 = random.choice(population)
        parent1 = population[rank_index[0] - 1]
        if parent1 == parent2 and population.count(parent1) == 1:
            while parent1 == parent2:
                parent2 = random.choice(population)
    else:
        print("Обираємо", rank_index[0], "та", rank_index[1], "за цінністю осіб")
        parent1 = population[rank_index[0] - 1]
        parent2 = population[rank_index[1] - 1]

    return parent1, parent2


def breed(parent1, parent2):
    global name_index
    parent1_chromosomes = lindexsplit(parent1, *crossover_points)
    parent2_chromosomes = lindexsplit(parent2, *crossover_points)

    print(parent1_chromosomes)
    print(parent2_chromosomes)

    children_chromosomes = transposed_cartesian(parent1_chromosomes, parent2_chromosomes)
    children_chromosomes.remove(parent1_chromosomes)
    children_chromosomes.remove(parent2_chromosomes)

    unique_list = []
    for x in children_chromosomes:
        if x not in unique_list:
            unique_list.append(x)
    children_chromosomes = deepcopy(unique_list)

    children = [list(itertools.chain.from_iterable(x)) for x in children_chromosomes]

    print("Можливі діти (", len(children), "):")
    for j in range(len(children)):
        print(children_chromosomes[j], end=' ')
        child_weight = sum([weights[i] for i in range(len(children[j])) if children[j][i] == 1])
        print("W =", ' + '.join([str(weights[i]) for i in range(len(children[j])) if children[j][i] == 1]), "=", child_weight, end='')
        if child_weight <= p:
            print(" ≤ P", end=' ')
            print("     F =", ' + '.join([str(values[i]) for i in range(len(children[j])) if children[j][i] == 1]), "=", fitness(children[j]))
        else:
            print(" > P")

    sorted_by_f = sorted(children, key=lambda x: fitness(x), reverse=True)
    descendant = sorted([el for el in sorted_by_f if fitness(el)==fitness(sorted_by_f[0])], key=lambda el: sum([weights[i] for i in range(len(el)) if el[i] == 1]))[0]
    print("Обираємо", [i+1 for i in range(len(children)) if descendant == children[i]][0], ':', descendant)
    return descendant


def mutate(individual):
    if mutation_type == 1 and iteration % 2 == 0 or mutation_type == 2 and iteration % 2 == 1 or mutation_type == 3:
        alt_individual = [1 for _ in individual]
        while fitness(alt_individual) == -1:
            alt_individual = deepcopy(individual)
            gene = random.randrange(len(individual))
            if alt_individual[gene] == 1:
                alt_individual[gene] = 0
            else:
                alt_individual[gene] = 1
        individual = alt_individual
        print("Проводимо мутацію, замінюємо", gene + 1, "ген -- отримали:")
        print(individual)
        new_weight = sum([weights[i] for i in range(len(individual)) if individual[i] == 1])
        print("W =", ' + '.join([str(weights[i]) for i in range(len(individual)) if individual[i] == 1]), "=", new_weight, end='')
        print("     F =", ' + '.join([str(values[i]) for i in range(len(individual)) if individual[i] == 1]), "=", fitness(individual))
    else:
        print("Мутацію не проводимо")
    return individual


def main():
    global iteration
    population = start_population
    name_index = start_name_index
    print_info()

    for _ in range(iterations):
        print()
        print(iteration, ')')
        if selection_type == 1:
            parent1, parent2 = tournament_select(population)
        elif selection_type == 2:
            parent1, parent2 = roulette_select(population, name_index)
        else:
            parent1, parent2 = ranked_select(population)

        print("Обираємо", end=' ')
        print([name_index[i] for i in range(len(population)) if population[i] == parent1][0], end=' і ')
        print([name_index[i] for i in range(len(population)) if population[i] == parent2][0])

        child = mutate(breed(parent1, parent2))
        to_be_deleted = sorted(population, key=lambda x: fitness(x), reverse=True)[-1]
        print("Видаляємо", [name_index[i] for i in range(len(population)) if population[i] == to_be_deleted][0], to_be_deleted)
        name_index.pop([i for i in range(len(population)) if population[i] == to_be_deleted][0])
        population = [x for x in population if x in sorted(population, key=lambda x: fitness(x), reverse=True)[:-1]]
        population.append(child)
        name_index.append('S' + str(len(population) + iteration))
        print("Додаємо", name_index[-1], child)
        iteration += 1

        print("Отримана популяція:")
        for i in range(len(population)):
            print(name_index[i], population[i], "F =", fitness(population[i]))


main()

