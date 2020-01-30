import xlrd
from xlrd.sheet import Sheet
import numpy as np
import matplotlib.pyplot as plt

category_names = [
    'Primary',
    'Secondary',
    'Future Plans',
    'No Plans'
]

results = {
    'Executives': [64,   27,  5,   4],
    'Middle Managers': [38  ,42  ,13  ,7],
    'Line Managers': [39    ,36  ,12  ,13],
    'Individual Contributors and Professionals': [33,    42  ,13  ,12],
    'Customers': [31    ,18  ,19  ,32],
    'Partners/Affiliates': [11  ,24  ,27  ,37],
    'Suppliers': [5.5   ,13  ,20.5    ,61]
}

'''
workbook = xlrd.open_workbook('test.xls')
print(workbook.sheet_names())
sheet: Sheet = workbook.sheet_by_index(0)
'''

def plot_svg(results, category_names):
    plt.clf()
    labels = list(results.keys())
    data = np.array(list(results.values()))
    print(data)
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

plot_svg(results, category_names)
