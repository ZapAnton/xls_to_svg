from pathlib import Path
from typing import List, Dict, Callable
import numpy as np
import matplotlib.pyplot as plt
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

    def __plot_bar_chart(self, input_data: InputFileData):
        raise NotImplementedError()

    def __plot_discrete_bar_chart(self, input_data: InputFileData):
        plt.clf()
        labels = list(input_data.data.keys())
        data = np.array(list(input_data.data.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(np.linspace(
            0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(9.2, 5))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname,
                color) in enumerate(zip(input_data.categories,
                                        category_colors)):
            widths = data[:, i]
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
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                ax.text(x,
                        y,
                        f'{c:g}',
                        ha='center',
                        va='center',
                        color=text_color)
        ax.legend(ncol=len(input_data.categories),
                  bbox_to_anchor=(0, 1),
                  loc='lower left',
                  fontsize='small')
        chart_filepath: Path = self.xls_filepath.parent / (
            self.xls_filepath.stem + '.svg')
        plt.savefig(chart_filepath)

    def __plot_stacked_bar_chart(self, input_data: InputFileData):
        raise NotImplementedError()

    def __plot_pie_chart(self, input_data: InputFileData):
        raise NotImplementedError()

    def __plot_donut_chart(self, input_data: InputFileData):
        raise NotImplementedError()

    def plot(self):
        input_data = InputFileData.from_file(self.xls_filepath)
        plot_method: Callable = self.__plot_method_mapping[self.chart_type]
        plot_method(input_data)
