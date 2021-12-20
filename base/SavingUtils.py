import xlwt


def writeExcel(sheetName: str, fileName: str, data: list):
    """
    This is a common approach for outputting and saving data collected from spy, i.e., Excel.
    All data will be saved in one sheet of a xls file.

    :param sheetName: sheetName of data
    :param fileName: file name of the saving data (including the path)
    :param data: a list of data items, the type of which must be dict.
    """
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(sheetName)

    # write header
    # we assume that every data has the same data structure
    row = 0
    for item in data:
        if row == 0:
            # write header
            col = 0
            for k in item:
                worksheet.write(row, col, label=str(k))
                col += 1
            row += 1

        col = 0
        for k in item:
            worksheet.write(row, col, label=str(item[k]))
            col += 1
        row += 1

    if not fileName.endswith('.xls'):
        fileName += '.xls'

    workbook.save(fileName)
