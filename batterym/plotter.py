#!/usr/bin/python
import log
import config
import unittest

from history import History
from future import Future
from chart import Chart

#import datetime  # TMP


def extract_plot_data(history, future):
    future.calculate_plot_data()
    xoffset = future.remaining_time()
    history.set_plot_data_xoffset(xoffset)
    history.set_plot_data_xlimit(hours=12.0)
    history.calculate_plot_data()
    return {
        'history charging': history.plot_data(['Charging', 'Full']),
        'history discharging': history.plot_data(['Discharging']),
        'future charging': future.plot_data(['Charging', 'Full']),
        'future discharging': future.plot_data(['Discharging']),
    }


def create_chart(plot_data, image_path):
    blue = '#2e7eb3'
    light_blue = '#81b1d1'
    green = '#4aa635'
    light_green = '#7db471'
    ylabels = ['0 %', '25 %', '50 %', '75%', '100 %']
    xlabels = [0, 2, 4, 6, 8, 10, '12 hours']
    plot = Chart(xlabels=xlabels, ylabels=ylabels,
                 inverseX=True, padding_top=30, height=450)
    plot.set_minimal_canvas([0, 0], [12, 100])

    for p in plot_data['history charging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=green, fill=green,
                 drop=green)

    for p in plot_data['history discharging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=blue, fill=blue,
                 drop=blue)

    for p in plot_data['future charging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=green, stroke_dash=True)

    for p in plot_data['future discharging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=blue, stroke_dash=True)

    plot.render_to_svg(image_path)


def caluclate_chart(image_path):
    smoothing = config.get_entry('smoothing', default_value=True)
    history = History(log.get_battery(), smoothing=smoothing)
    future = Future(history)
    plot_data = extract_plot_data(history, future)
    # life_time = datetime.timedelta(
    #     seconds=future.battery_life()*60*60)
    # remaining_life_time = datetime.timedelta(
    #     seconds=future.remaining_time()*60*60)
    # print life_time, remaining_life_time
    create_chart(plot_data, image_path)


# def main():
#     caluclate_chart('capacity_history_12h.svg')


# if __name__ == '__main__':
#     main()
