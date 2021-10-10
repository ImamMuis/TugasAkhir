import openpyxl 
  
dataMasuk = 'data/userMasuk.xlsx'
wb_obj = openpyxl.load_workbook(dataMasuk) 
sheet_obj = wb_obj.active 
cell_obj = sheet_obj['A2': 'E6']
print('Pendeteksian | User | Hari   | Tanggal    | Jam')

for cell1, cell2, cell3, cell4, cell5 in cell_obj:
    print(cell1.value, cell2.value, cell3.value, cell4.value, cell5.value)