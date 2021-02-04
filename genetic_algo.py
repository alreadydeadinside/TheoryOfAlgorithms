##################################Задача про рюкзак#############################################
def knapSack(W, wt, val):
    n = len(val)
    table = [[0 for x in range(W + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for j in range(W + 1):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif wt[i - 1] <= j:
                table[i][j] = max(val[i - 1]
                                  + table[i - 1][j - wt[i - 1]], table[i - 1][j])
            else:
                table[i][j] = table[i - 1][j]

    return table[n][W], table

'''1, 2, 4 '''
cost = [5, 7, 8, 6, 4, 1]
weight = [2, 3, 4, 3, 2, 1]
W = 8

print(knapSack(W, weight, cost)[0])

for i in knapSack(W, weight, cost)[1]:
    print(i)
#################################Задача про рюкзак#################################################



##################################Генетический алгоритм#############################################
def crossover_one_point(parent1, parent2):
    VerNumber = len(parent1)
    center = int(VerNumber / 2)
    individual1 = parent1[:center] + parent2[center:]
    individual2 = parent2[:center] + parent1[center:]
    return individual1, individual2


def crossover_two_point(parent1, parent2):
    VerNumber = len(parent1)
    center = int(VerNumber / 3)
    individual1 = parent1[:center] + parent1[center:center * 2] + parent2[center * 2:]
    individual2 = parent1[:center] + parent2[center:center * 2] + parent2[center * 2:]
    individual3 = parent1[:center] + parent2[center:center * 2] + parent1[center * 2:]
    individual4 = parent2[:center] + parent2[center:center * 2] + parent1[center * 2:]
    individual5 = parent2[:center] + parent1[center:center * 2] + parent1[center * 2:]
    individual6 = parent2[:center] + parent1[center:center * 2] + parent2[center * 2:]
    return individual1, individual2, individual3, individual4, individual5, individual6

def check_children(childrens):
    for i in childrens:
        current_weight = 0
        current_cost = 0
        for j in range(len(i)):
            if i[j] == 1:
                current_weight += weight[j]
                current_cost += cost[j]
        if current_weight > W:
            print(f'{i}  cost:{current_cost}, weight:{current_weight} - children died')
        else:
            print(f'{i}  cost:{current_cost}, weight:{current_weight}')

check_children(crossover_two_point([0, 1, 1, 0, 0, 0], [1, 0, 1, 0, 1, 1]))
##################################Генетический алгоритм#############################################
