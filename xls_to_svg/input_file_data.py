from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
import xlrd
from xlrd.sheet import Sheet
from xlrd.book import Book


@dataclass
class InputFileData:
    categories: List[str]
    data: Dict[str, List[float]]

    @classmethod
    def from_file(cls, filepath: Path):
        workbook: Book = xlrd.open_workbook(filepath)
        sheet: Sheet = workbook.sheet_by_index(0)
        categories: List[str] = [cell.value for cell in sheet.row(0)][1:]
        data: Dict[str, List[float]] = {
            sheet.row(row_num)[0].value:
            [cell.value for cell in sheet.row(row_num)[1:]]
            for row_num in range(1, sheet.nrows)
        }
        return cls(categories, data)
