from dataclasses import dataclass
from typing import List
from pathlib import Path
import xlrd
from xlrd.sheet import Sheet, Cell
from xlrd.book import Book


@dataclass
class InputFileRow:
    label: str
    values: List[float]

    @classmethod
    def from_xls_row(cls, row: List[Cell]):
        label: str = row[0].value
        values: List[float] = [cell.value for cell in row[1:]]
        input_file_row = cls(label, values)
        return input_file_row


@dataclass
class InputFileData:
    categories: List[str]
    rows: List[InputFileRow]

    @classmethod
    def from_file(cls, filepath: Path):
        workbook: Book = xlrd.open_workbook(filepath)
        sheet: Sheet = workbook.sheet_by_index(0)
        categories: List[str] = [cell.value for cell in sheet.row(0)][1:]
        data: List[InputFileRow] = [
            InputFileRow.from_xls_row(sheet.row(row_num))
            for row_num in range(1, sheet.nrows)
        ]
        return cls(categories, data)
