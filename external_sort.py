import math
from copy import deepcopy

sort_types = {1: 'пряме злиття',
              2: 'природне злиття',
              3: 'збалансоване багатошляхове злиття',
              4: 'багатофазне сортування'}


#                       SELECT HERE~~~~~~~~~~~~~~~~~~~~~~~~~~~

sort_type = 1

file_a = [22, 42, 8, 15, 13, 17, 41, 21, 24, 25, 2, 35, 19, 49, 76,
          99, 6, 9, 31, 12, 54, 16, 23, 68, 77, 1, 71, 86, 6, 87]

#                      SELECT HERE~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Застосуємо", sort_types[sort_type], "для сортування записів")
print("A:", file_a)


def direct_merge_external_sort(file_a):
    iteration = 1
    last_iteration = math.ceil(math.log2(len(file_a)))
    while iteration <= last_iteration:
        series_length = pow(2, iteration - 1)
        print(iteration, ")")

        print("Розділ")
        file_b, file_c = [], []
        for k in range(len(file_a)):
            if int(k / series_length) % 2 == 0:
                file_b.append(file_a[k])
            else:
                file_c.append(file_a[k])
        print("B:", file_b)
        print("C:", file_c)

        print("Злиття")
        file_a = []
        combined_ordered = []
        i = 0
        while i < max(len(file_b), len(file_c)):
            for j in range(series_length):
                if i < len(file_b):
                    combined_ordered.append(file_b[i])
                if i < len(file_c):
                    combined_ordered.append(file_c[i])
                i += 1
            combined_ordered = sorted(combined_ordered)
            for elem in combined_ordered:
                file_a.append(elem)
            combined_ordered = []

        print("A:", file_a)
        print()
        iteration += 1
    return file_a


def natural_merge_external_sort(file_a):
    iteration = 1
    while file_a != sorted(file_a):
        print(iteration, ")")

        print("Розділ")
        file_b, file_c = [], []
        serie = []
        series = []
        serie_last = None
        for n in range(len(file_a)):
            if serie_last is None or file_a[n] >= serie_last:
                serie_last = file_a[n]
                serie.append(serie_last)
            else:
                series.append(serie)
                serie_last = file_a[n]
                serie = [serie_last]
        if serie:
            series.append(serie)

        for i in range(len(series)):
            if i % 2 == 0:
                for elem in series[i]:
                    file_b.append(elem)
            else:
                for elem in series[i]:
                    file_c.append(elem)

        print("B:", file_b)
        print("C:", file_c)

        print("Злиття")
        file_a = []
        for i in range(0, len(series), 2):
            superserie = []
            for elem in series[i]:
                superserie.append(elem)
            if i+1 < len(series):
                for elem in series[i+1]:
                    superserie.append(elem)
            superserie = sorted(superserie)
            for elem in superserie:
                file_a.append(elem)
        print("A:", file_a)
        print()
        iteration += 1
    return file_a


def balanced_threeway_merge_external_sort(file_a):
    print('1 )')
    x1, x2, x3 = [], [], []
    serie = []
    series = []
    serie_last = None
    for n in range(len(file_a)):
        if serie_last is None or file_a[n] >= serie_last:
            serie_last = file_a[n]
            serie.append(serie_last)
        else:
            series.append(serie)
            serie_last = file_a[n]
            serie = [serie_last]
    if serie:
        series.append(serie)

    for i in range(len(series)):
        if i % 3 == 0:
            x1.append(series[i])
        elif i % 3 == 1:
            x2.append(series[i])
        else:
            x3.append(series[i])

    print("X1:", x1)
    print("X2:", x2)
    print("X3:", x3)
    iteration = 2
    while x1 != [sorted(file_a)]:
        print(iteration, ')')
        x1_new, x2_new, x3_new = [], [], []
        for i in range(max(len(x1), len(x2), len(x3))):
            if i < len(x3):
                superserie = sorted(x1[i] + x2[i] + x3[i])
                if i % 3 == 0:
                    x1_new.append(superserie)
                elif i % 3 == 1:
                    x2_new.append(superserie)
                else:
                    x3_new.append(superserie)
            elif i < len(x2):
                superserie = sorted(x1[i] + x2[i])
                if i % 3 == 0:
                    x1_new.append(superserie)
                elif i % 3 == 1:
                    x2_new.append(superserie)
                else:
                    x3_new.append(superserie)
            else:
                superserie = deepcopy(x1[i])
                if i % 3 == 0:
                    x1_new.append(superserie)
                elif i % 3 == 1:
                    x2_new.append(superserie)
                else:
                    x3_new.append(superserie)

        x1, x2, x3 = deepcopy(x1_new), deepcopy(x2_new), deepcopy(x3_new)
        print("X1:", x1)
        print("X2:", x2)
        print("X3:", x3)
        iteration +=1

    file_a = x1[0]
    print()
    print('A:', file_a)
    return file_a


def polyphasic_external_sort(file_a):
    serie = []
    series = []
    serie_last = None
    for n in range(len(file_a)):
        if serie_last is None or file_a[n] >= serie_last:
            serie_last = file_a[n]
            serie.append(serie_last)
        else:
            series.append(serie)
            serie_last = file_a[n]
            serie = [serie_last]
    if serie:
        series.append(serie)
    print(len(series), 'серій в файлі')

    distributions = [(int(len(series)/2), len(series)-int(len(series)/2))]
    for i in range(distributions[0][0]-1):
        distributions.append((distributions[0][0]-1-i, len(series)-(distributions[0][0]-1-i)))

    def attempt_distribution(distribution):
        print("Застосуємо розподіл", distribution[0], distribution[1], 0)
        print('1 )')
        x1, x2, x3 = [], [], []
        for i in range(len(series)):
            if i < distribution[0]:
                x1.append(series[i])
            else:
                x2.append(series[i])

        print("X1:", x1)
        print("X2:", x2)
        print("X3:", x3)
        iteration = 2

        while not ((len(x1) == 0 and len(x2) == 0) or (len(x1) == 0 and len(x3) == 0) or (len(x2) == 0 and len(x3) == 0)):
            print(iteration, ')')

            if len(x3) == 0:
                if len(x1) > len(x2):
                    for i in range(len(x2)):
                        superserie = sorted(x1[i] + x2[i])
                        x3.append(superserie)
                    x1 = x1[len(x2):]
                    x2 = []
                else:
                    for i in range(len(x1)):
                        superserie = sorted(x1[i] + x2[i])
                        x3.append(superserie)
                    x2 = x2[len(x1):]
                    x1 = []

            elif len(x2) == 0:
                if len(x1) > len(x3):
                    for i in range(len(x3)):
                        superserie = sorted(x1[i] + x3[i])
                        x2.append(superserie)
                    x1 = x1[len(x3):]
                    x3 = []
                else:
                    for i in range(len(x1)):
                        superserie = sorted(x1[i] + x3[i])
                        x2.append(superserie)
                    x3 = x3[len(x1):]
                    x1 = []

            else:
                if len(x2) > len(x3):
                    for i in range(len(x3)):
                        superserie = sorted(x2[i] + x3[i])
                        x1.append(superserie)
                    x2 = x2[len(x3):]
                    x3 = []
                else:
                    for i in range(len(x2)):
                        superserie = sorted(x2[i] + x3[i])
                        x1.append(superserie)
                    x3 = x3[len(x2):]
                    x2 = []

            print("X1:", x1)
            print("X2:", x2)
            print("X3:", x3)
            iteration += 1

        return x1, x2, x3

    x1, x2, x3 = None, None, None
    for option in distributions:
        if x1 != [sorted(file_a)] and x2 != [sorted(file_a)] and x3 != [sorted(file_a)]:
            if option != distributions[0]:
                print("Розподіл", option[0]+1, option[1]-1, 0, "не зводиться!!")
                print()
            x1, x2, x3 = attempt_distribution(option)
        else:
            print("Розподіл", option[0]+1, option[1]-1, 0, "зводиться")
            break

    print()
    print('A:', sorted(file_a))
    return sorted(file_a)


def main():
    if sort_type == 1:
        direct_merge_external_sort(file_a)
    elif sort_type == 2:
        natural_merge_external_sort(file_a)
    elif sort_type == 3:
        balanced_threeway_merge_external_sort(file_a)
    else:
        polyphasic_external_sort(file_a)


main()
