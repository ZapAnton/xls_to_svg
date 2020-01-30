import xlrd
from dataclasses import dataclass
from xlrd.sheet import Sheet, Cell
from xlrd.book import Book
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt


DEFAULT_FILE_NAME = 'data.xls'

@dataclass
class ExcelData:
    categories: List[str]
    data: Dict[str, List[float]]


    @classmethod
    def from_xls(cls, workbook: Book):
        sheet: Sheet = workbook.sheet_by_index(0)
        categories: List[str] = [cell.value for cell in sheet.row(0)][1:]
        data: Dict[str, List[float]] = {
            sheet.row(row_num)[0].value: [cell.value for cell in sheet.row(row_num)[1:]]
            for row_num in range(1, sheet.nrows)
        }
        return cls(categories, data)

def plot_svg(results, category_names):
    plt.clf()
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    plt.savefig('test.svg')


workbook = xlrd.open_workbook(DEFAULT_FILE_NAME)
excel_data = ExcelData.from_xls(workbook)
plot_svg(excel_data.data, excel_data.categories)
