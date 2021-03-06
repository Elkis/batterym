#!/usr/bin/python
from __future__ import division
from history import separate_by_sequence_id
import unittest


def median(lst):
    n = len(lst)
    if n < 1:
        return 0
    lst = sorted(lst)
    m = int(n/2)
    if n % 2 == 1:
        return lst[m]
    return (lst[m-1] + lst[m])/2


def is_zero(val, abs_tol=1e-9):
    return abs(val) < abs_tol


def line_plot_data(y, slope):
    # y = slope * x + b, b=0
    # x = y / slope
    # slope = 100 / life
    x = y / slope
    x = abs(x)
    status = None
    if 0 < slope:
        status = 'Discharging'
        ys = [0, y]
        xs = [0, x]
    else:
        status = 'Charging'
        dy = 100.0 - y
        x = -dy / slope
        xs = [0, x]
        ys = [100, y]
    return {
        'status': status,
        'xs': xs,
        'ys': ys,
    }


class Future:

    def __init__(self, history):
        self._history = history
        self._plot_data = []

    def calculate_plot_data(self):
        self._plot_data = []
        data = self.current_status_data()
        slope = self.calculate_slope(data)
        if slope is None or is_zero(slope):
            return
        self._battery_life = 100.0 / abs(slope)
        y = data[0]['capacity']
        self._plot_data = [line_plot_data(y, slope)]

    def remaining_time(self):
        x = 0
        for d in self._plot_data:
            x = max(x, max(d['xs']))
        return x

    def battery_life(self):
        return self._battery_life

    def plot_data(self, status):
        return [x for x in self._plot_data if x.get('status') in status]

    def current_status_data(self):
        time_limit_hour = 10.0 / 60.0
        data = self._history.get_recent_history(time_limit_hour)
        batches = separate_by_sequence_id(data)
        return batches[0] if len(batches) > 0 else None

    def calculate_slope(self, data):
        slopes = []
        for i in xrange(1, len(data)):
            dy = data[i]['capacity'] - data[0]['capacity']
            dx = data[i]['virtual_time_hour'] - data[0]['virtual_time_hour']
            if not is_zero(dx):
                slopes.append(dy / dx)
        return median(slopes)


class MyTest(unittest.TestCase):

    def test_median(self):
        self.assertEqual(median([]), 0)
        self.assertEqual(median([1]), 1)
        self.assertEqual(median([1, 3]), 2)
        self.assertEqual(median([1, 3, 4]), 3)

    def test_is_zero(self):
        self.assertEqual(is_zero(1e-7, abs_tol=1e-3), True)
        self.assertEqual(is_zero(1e-3, abs_tol=1e-7), False)

    def test_line_plot_data(self):
        self.assertEqual(line_plot_data(42, 100.0/10),
            {'status': 'Discharging', 'xs': [0, 4.2], 'ys': [0, 42]})

        self.assertEqual(line_plot_data(42, -100.0/2),
            {'status': 'Charging', 'xs': [0, 1.16], 'ys': [100, 42]})
