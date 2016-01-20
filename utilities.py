import pygame
import math


def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


def get_vector(self, a, b, x, y):

    distance_to_target = distance(a, b, x, y)
    factor = distance_to_target / self.speed
    x_dist = a - x
    y_dist = b - y
    if factor == 0:
        factor = 1
    change_x = x_dist / factor
    change_y = y_dist / factor
    change_x = round(change_x)
    change_y = round(change_y)

    return (change_x, change_y)
