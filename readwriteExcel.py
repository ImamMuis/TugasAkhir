import openpyxl 
dataMasuk = 'data/userMasuk.xlsx'
wb = openpyxl.load_workbook(dataMasuk) 
sheet = wb.active 
maxRow = sheet.max_row
count1 = maxRow
newdata = [[count1, 'Imam', 'Sun', '21-09-2021', '18:00:00']]
  
for row in newdata:
    sheet.append(row)
  
wb.save(dataMasuk)