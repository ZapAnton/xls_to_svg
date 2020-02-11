from pathlib import Path
from typing import List, Dict, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from xls_to_svg.input_file_data import InputFileData


class ChartPlotter:

    CHART_TYPES: List[str] = [
        'bar_chart', 'discrete_bar_chart', 'stacked_bar_chart', 'pie_chart',
        'donut_chart'
    ]

    def __init__(self, chart_type: str, xls_filepath: Path):
        self.chart_type: str = chart_type
        self.xls_filepath: Path = xls_filepath
        self.__plot_method_mapping: Dict[str, Callable] = {
            'bar_chart': self.__plot_bar_chart,
            'discrete_bar_chart': self.__plot_discrete_bar_chart,
            'stacked_bar_chart': self.__plot_stacked_bar_chart,
            'pie_chart': self.__plot_pie_chart,
            'donut_chart': self.__plot_donut_chart,
        }

    def __plot_bar_chart(self, input_data: InputFileData) -> Figure:
        plt.clf()
        values: List[float] = input_data.rows[0].values
        label_ticks = range(len(values))
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.barh(label_ticks, values, align='center')
        ax.set_yticks(label_ticks)
        ax.set_yticklabels(input_data.categories)
        ax.tick_params(length=0)
        ax.set_frame_on(False)
        ax.invert_yaxis()
        return fig

    def __plot_discrete_bar_chart(self, input_data: InputFileData) -> Figure:
        plt.clf()
        labels: List[str] = [input_row.label for input_row in input_data.rows]
        data = np.array([input_row.values for input_row in input_data.rows])
        totals = np.sum(data, axis=1)
        data_totals = np.array(
            [row / total * 100 for row, total in zip(data, totals)])
        data_cum = data_totals.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(np.linspace(
            0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(14, 5))
        ax.invert_yaxis()
        ax.set_frame_on(False)
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data_totals, axis=1).max())
        ax.tick_params(length=0)

        for i, (colname,
                color) in enumerate(zip(input_data.categories,
                                        category_colors)):
            widths_old = data[:, i]
            widths = data_totals[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(labels,
                    widths,
                    left=starts,
                    height=0.5,
                    label=colname,
                    color=color)
            xcenters = starts + widths / 2
            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            for y, (x, c) in enumerate(zip(xcenters, widths_old)):
                ax.text(x,
                        y,
                        f'{c:g}',
                        ha='center',
                        va='center',
                        color=text_color)
        ax.legend(ncol=len(input_data.categories),
                  bbox_to_anchor=(0, 1),
                  loc='lower left',
                  fontsize='small',
                  frameon=False)
        return fig

    def __plot_stacked_bar_chart(self, input_data: InputFileData) -> Figure:
        plt.clf()
        labels: List[str] = [input_row.label for input_row in input_data.rows]
        fig, ax = plt.subplots(figsize=(14, 5))
        data = np.array([input_row.values for input_row in input_data.rows])
        data_cum = data.cumsum(axis=1)
        for i, category in enumerate(input_data.categories):
            bottom = data_cum[:, i - 1] if i != 0 else 0
            ax.bar(labels, data[:, i], 0.4, bottom=bottom, label=category)
        plt.subplots_adjust(right=0.7)
        ax.legend(loc='best',
                  bbox_to_anchor=(1, 0.5),
                  fontsize='small',
                  frameon=False)
        ax.tick_params(length=0)
        ax.set_frame_on(False)
        return fig

    def __plot_pie_chart(self, input_data: InputFileData) -> Figure:
        plt.clf()
        values: List[float] = input_data.rows[0].values
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.pie(values, autopct='%1.2f')
        plt.subplots_adjust(right=0.4)
        ax.axis('equal')
        ax.legend(input_data.categories,
                  loc='best',
                  bbox_to_anchor=(1, 0.5),
                  fontsize='small',
                  frameon=False)
        return fig

    def __plot_donut_chart(self, input_data: InputFileData) -> Figure:
        raise NotImplementedError()

    def plot(self):
        input_data = InputFileData.from_file(self.xls_filepath)
        plot_method: Callable = self.__plot_method_mapping[self.chart_type]
        chart: Figure = plot_method(input_data)
        chart_filepath: Path = self.xls_filepath.parent / (
            self.xls_filepath.stem + '.svg')
        chart.savefig(chart_filepath)
