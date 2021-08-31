# Install xlrd by using pip
import xlrd

book = xlrd.open_workbook_xls('Copie_de_Themes.xls', formatting_info=True)
sheets = book.sheet_names()

txt = ''
with open('list.txt', 'w') as to_write:
    for line, sh in enumerate(sheets):
        sheet_line = book.sheet_by_index(line)
        # Get rows number
        rows = sheet_line.nrows
        
        # iterate each other
        for row in range(rows):
            # Do what you want for each row
            xfc = sheet_line.cell_xf_index(row, 0)
            xf = book.xf_list[xfc]
            value = sheet_line.cell_value(row, 0)
            bg = xf.background.pattern_colour_index
            print(value, row, bg)
    to_write.write(txt)
