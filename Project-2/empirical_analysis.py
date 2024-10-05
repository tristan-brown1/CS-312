import random

from byu_pytest_utils import max_score

from test_utils import is_convex_hull
import matplotlib.pyplot as plt
from convex_hull import compute_hull
from generate import generate_random_points
# from plotting import draw_line,draw_hull,plot_points,show_plot,title
from time import time

n_list = [10, 100, 1000, 10000, 100000, 500000, 1000000]


def plot_points(points: list[tuple[float, float]], **kwargs):
    if 'c' not in kwargs:
        kwargs['c'] = 'k'

    xx, yy = zip(*points)
    plt.scatter(xx, yy, **kwargs)


def draw_hull(points: list[tuple[float, float]], **kwargs):
    xx, yy = zip(*points)
    xx = [*xx, points[0][0]]
    yy = [*yy, points[0][1]]
    plt.plot(xx, yy, **kwargs)

def draw_line(p1: tuple[float, float], p2: tuple[float, float], **kwargs):
    xx = [p1[0], p2[0]]
    yy = [p1[1], p2[1]]
    plt.plot(xx, yy, **kwargs)


def circle_point(point: tuple[float, float], **kwargs):
    for k, v in {
        's': 80,
        'facecolors': 'none',
        'edgecolors': 'r'
    }.items():
        if k not in kwargs:
            kwargs[k] = v
    plt.scatter(point[0], point[1], **kwargs)


title = plt.title

show_plot = plt.show
# def test_guassian_distribution_large(n,seed):
#     points = generate_random_points('guassian', n, seed)
#     candidate_hull = compute_hull(points)
#     assert is_convex_hull(candidate_hull, points)
#
# def test_main():
#     for n in n_list:
#         test_guassian_distribution_large(n,312)
#         test_guassian_distribution_large(n,418)
#         test_guassian_distribution_large(n,428)
#         test_guassian_distribution_large(n,438)
#         test_guassian_distribution_large(n,448)



if __name__ == '__main__':

    elapsed_time = []
    for value in n_list:
        for i in range(5):
            seed = random.randint(1,500)
            points = generate_random_points("normal", value, seed)
            plot_points(points)

            start = time()
            hull_points = compute_hull(points)
            end = time()

            elapsed_time.append(round(end - start, 4))

            draw_hull(hull_points)
            title(f'{value} normal points: {round(end - start, 4)} seconds')
            show_plot()


def test2():
    import numpy as np
    import matplotlib.pyplot as plt

    # creating the dataset
    data = {'10': 0.00198, '100': 0.00334, '1000': 0.0154,
            '10000': 0.1315, '100000': 1.28692,'500000': 7.07606,'1000000': 16.9988}
    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(courses, values, color='indigo',
            width=0.4)

    plt.xlabel("Number of Points")
    plt.ylabel("Mean Runtime in Seconds")
    plt.title("Mean Runtimes Depending on Number of Points")
    plt.show()

def test3():
    import numpy as np
    import matplotlib.pyplot as plt

    # creating the dataset
    data = {'10': 10, '100': 200, '1000': 3000,
            '10000': 40000, '100000': 500000, '500000': 2849485.002, '1000000': 6000000}
    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(courses, values, color='green',
            width=0.4)

    plt.xlabel("Values of N")
    plt.ylabel("F(NlogN)")
    plt.title("F(NlogN) for Different Values of N")
    plt.show()