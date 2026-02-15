import openpyxl

wb = openpyxl.load_workbook(r'D:\Django Project\Alto Project\alto files\K1 Power Levels.xlsx')
sheet = wb.active

print('=== Sheet Name ===')
print(sheet.title)
print()

print('=== Headers (Row 1) ===')
for i, cell in enumerate(sheet[1]):
    if cell.value:
        print(f"  Column {cell.column_letter} ({i}): {cell.value}")

print()
print('=== Data for SonOfZeus (Row 2) ===')
for i, cell in enumerate(sheet[2]):
    header = sheet[1][i].value
    if header:
        print(f"  {cell.column_letter}. {header}: {cell.value}")

print()
print('=== Formula in SCORE column ===')
# Find SCORE column
for i, cell in enumerate(sheet[1]):
    if cell.value and 'SCORE' in str(cell.value).upper():
        score_cell = sheet.cell(row=2, column=i+1)
        print(f"  Column {score_cell.column_letter}: Value = {score_cell.value}")
        if hasattr(score_cell, 'value') and score_cell.data_type == 'f':
            print(f"  Formula: {score_cell.value}")
