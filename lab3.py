import functools
import math
import re
import matplotlib.pyplot as plt
from random import randint


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'x:' + str(self.x) + ' y:' + str(self.y)

    def get_distance(self, point):
        return math.sqrt(((self.x - point.x) ** 2) + ((self.y - point.y) ** 2))


class Cluster:
    def __init__(self, x, y):
        self.center = Point(x, y)
        self.points = []

    def __repr__(self):
        return 'center:' + self.center.__repr__()


def main():
    file = open('datasets/birch3.txt', 'r')
    lines = file.readlines()
    points = []
    clusters = []
    for x in range(5):
        cluster = Cluster(randint(0, 10000), randint(0, 10000))
        clusters.append(cluster)
    for line in lines:
        nums = re.split('\\s+', line)
        point = Point(int(nums[1]), int(nums[2]))
        points.append(point)
    lengths = []
    while True:
        add_to_clusters(clusters, points)
        is_end = True
        if len(lengths) == 0:
            is_end = False
        for i in range(len(lengths)):
            if not (lengths[i] == len(clusters[i].points)):
                is_end = False
                break
        if is_end:
            break
        evaluate_new_centers(clusters)
        lengths.clear()
        for cluster in clusters:
            lengths.append(len(cluster.points))
            cluster.points.clear()
    for point in clusters[0].points:
        plt.plot(point.x, point.y, 'o', color='black')

    for point in clusters[1].points:
        plt.plot(point.x, point.y, 'o', color='red')

    for point in clusters[2].points:
        plt.plot(point.x, point.y, 'o', color='blue')

    for point in clusters[3].points:
        plt.plot(point.x, point.y, 'o', color='green')
    plt.show()


def evaluate_new_centers(clusters):
    for cluster in clusters:
        if len(cluster.points) > 0:
            cluster.center.y = functools.reduce(lambda a, b: a + b, list(map(lambda q: q.y, cluster.points))) / len(
                cluster.points)
            cluster.center.x = functools.reduce(lambda a, b: a + b, list(map(lambda q: q.x, cluster.points))) / len(
                cluster.points)


def add_to_clusters(clusters, points):
    for point in points:
        best_cluster = None
        for cluster in clusters:
            if best_cluster is None or cluster.center.get_distance(point) < best_cluster.center.get_distance(point):
                best_cluster = cluster
        best_cluster.points.append(point)


main()
