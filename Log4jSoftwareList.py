# made with love by Milad Khoshdel for personal use
# https://regux.com

import requests
from bs4 import BeautifulSoup
import xlsxwriter

page = requests.get("https://github.com/NCSC-NL/log4shell/blob/main/software/README.md")
soup = BeautifulSoup(page.content, 'html.parser')

all_tables = soup.find_all('table')

result = {}

for table in all_tables:
    header = table.find("thead").get_text()
    if "Supplier" in header:
        hole_table = table.find_all('tbody')
        for item in hole_table:
            hole_tr = item.find_all('tr')
            for tr in hole_tr:
                hole_tds = tr.find_all('td')
                if "Not" not in hole_tds[3].get_text():
                    if hole_tds[0].get_text() not in result.keys():
                        result[hole_tds[0].get_text()] = [hole_tds[1].get_text()]
                    else:
                        result[hole_tds[0].get_text()].append(hole_tds[1].get_text())

row = 0
column = 0

workbook = xlsxwriter.Workbook('log4J_Vulnerabilities.xlsx')
worksheet = workbook.add_worksheet()
header_list = list(result.keys())
for header in header_list:
    row = 0
    worksheet.write(row, column, header)
    vuln_list = list(result[header])
    for vulnerability in vuln_list:
        row = row + 1
        worksheet.write(row, column, vulnerability)
    column = column + 1
workbook.close()
