from typing import List


class ChartPlotter:

    CHART_TYPES: List[str] = [
        'bar_chart', 'stacked_bar_chart', 'pie_chart', 'donut_chart'
    ]

    def __init__(self, chart_type: str, xls_filepath: str):
        self.chart_type: str = chart_type
        self.xls_filepath: str = xls_filepath

    def plot(self):
        print(self.xls_filepath)
