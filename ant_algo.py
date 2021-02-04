##################################Муравьиный алгоритм#############################################
top_vertice = 5
alpha = 2
beta = 3
p = 0.2
D = [[-1, 1, 7, 3, 14],
    [3, -1, 6, 9, 1],
    [6, 14, -1, 3, 7],
    [2, 3, 5, -1, 9],
    [15, 7, 11, 2, -1]]


def Dji():
    Dji = [[-1, 1, 7, 3, 14],
            [3, -1, 6, 9, 1],
            [6, 14, -1, 3, 7],
            [2, 3, 5, -1, 9],
            [15, 7, 11, 2, -1]]
    for i in range(len(Dji)):
        for j in range(len(Dji)):
            Dji[i][j] = round(1 / Dji[i][j], 3)
    return Dji

Tij = [[0, 0.2, 0.1, 0.1, 0.2],
       [0.1, 0, 0.3, 0.2, 0.1],
       [0.3, 0.3, 0, 0.3, 0.3],
       [0.3, 0.2, 0.3, 0, 0.3],
       [0.2, 0.3, 0.1, 0.3, 0]]


all_path = [1, 2, 3, 4, 5, 1]
def count_Lmin(path):
    l_min = 0
    for i in range(len(D)):
        l_min += D[path[i]-1][path[i+1]-1]
    return l_min

for i in Dji():
    print(i)

for i in D:
    print(i)

print(count_Lmin(all_path))

def count_probability(i, j, accepatble_nodes):
    sum_ = sum([((Tij[i-1][j-1])**alpha)*((Dji()[i-1][j-1])**beta) for j in accepatble_nodes])
    Pij = ((Tij[i-1][j-1])**alpha)*((Dji()[i-1][j-1])**beta) / sum_
    return Pij

print(count_probability(5, 4, [3, 4]))

"""Нашли маршрут, нашли его длину
Пересчитываем концентрацию феромона"""

def referomon():
    Tij_new = [[0]* top_vertice for _ in range(top_vertice)]
    path = [1, 2, 5, 4, 3, 1]
    new_path = []
    for i in range(len(path)-1):
        new_path.append((path[i], path[i + 1]))

    for i in range(len(Tij_new)):
        for j in range(len(Tij_new)):
            if (i + 1, j + 1) in new_path:
                print(f'Tij_new{i,j}, (1-p)*Tij[i][j] + {(count_Lmin(all_path)/count_Lmin(path))} = {round((1-p)*Tij[i][j] + (count_Lmin(all_path)/count_Lmin(path)), 3)}')
                Tij_new[i][j] = round((1-p)*Tij[i][j] + (count_Lmin(all_path)/count_Lmin(path)), 3)
            else:
                print(f'Tij_new{i,j}, (1-p)*Tij[i][j] = {round((1 - p) * Tij[i][j], 3)}')
                Tij_new[i][j] = round((1 - p) * Tij[i][j], 3)

    for i in Tij_new:
        print(i)


referomon()


def dual_referomon():
    Tij_new = [[0]* top_vertice for _ in range(top_vertice)]
    first_path = [1, 2, 5, 4, 3, 1]
    second_path = [2, 1, 5, 4, 3, 2]
    new_first_path = []
    new_second_path = []
    for i in range(len(first_path)-1):
        new_first_path.append((first_path[i], first_path[i + 1]))

    for i in range(len(second_path)-1):
        new_second_path.append((second_path[i], second_path[i + 1]))

    print(new_first_path)

    print(new_second_path)

    for i in range(len(Tij_new)):
        for j in range(len(Tij_new)):
            if (i + 1, j + 1) in new_first_path and new_second_path:
                print(f'Tij_new{i + 1,j + 1}, (1-p)*Tij[i][j] + {count_Lmin(all_path)/count_Lmin(first_path)} + {count_Lmin(all_path)/count_Lmin(second_path)} = {round((1-p)*Tij[i][j] + (count_Lmin(all_path)/count_Lmin(first_path) + count_Lmin(all_path)/count_Lmin(second_path)), 3)}')
                Tij_new[i][j] = round((1-p)*Tij[i][j] + (count_Lmin(all_path)/count_Lmin(first_path) + count_Lmin(all_path)/count_Lmin(second_path)), 3)

            elif (i + 1, j + 1) in new_first_path:
                print(f'Tij_new{i + 1,j + 1}, (1-p)*Tij[i][j] + {count_Lmin(all_path)/count_Lmin(first_path)} = {round((1 - p) * Tij[i][j] + count_Lmin(all_path)/count_Lmin(first_path), 3)}')
                Tij_new[i][j] = round((1 - p) * Tij[i][j] + count_Lmin(all_path)/count_Lmin(first_path), 3)

            elif (i + 1, j + 1) in new_second_path:
                print(f'Tij_new{i + 1,j + 1}, (1-p)*Tij[i][j] + {count_Lmin(all_path)/count_Lmin(second_path)} = {round((1 - p) * Tij[i][j] + count_Lmin(all_path)/count_Lmin(second_path), 3)}')
                Tij_new[i][j] = round((1 - p) * Tij[i][j] + count_Lmin(all_path)/count_Lmin(second_path), 3)

            else:
                print(f'Tij_new{i + 1,j + 1}, (1-p)*Tij[i][j] = {round((1 - p) * Tij[i][j], 3)}')
                Tij_new[i][j] = round((1 - p) * Tij[i][j], 3)

    for i in Tij_new:
        print(i)

dual_referomon()
