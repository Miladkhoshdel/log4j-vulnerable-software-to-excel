# made with love by Milad Khoshdel for personal use
# https://regux.com
# Edited by Mehdi Bastani

import requests
from bs4 import BeautifulSoup
import xlsxwriter
from string import ascii_lowercase

ind = list(ascii_lowercase)
ind.insert(0, '0-9')

result = {}
for i in range(27):
    page = requests.get(f'https://github.com/NCSC-NL/log4shell/blob/main/software/software_list_{ind[i]}.md')
    soup = BeautifulSoup(page.content, 'html.parser')

    get_table = soup.find('table')
    whole_table = get_table.find('tbody')
    rows = whole_table.find_all('tr')

    for tr in rows:
        whole_tds = tr.find_all('td')
        tmpList = [whole_tds[i].get_text() for i in range(3, 7)]
        if ("Vulnerable" not in tmpList) and ("Workaround" not in tmpList) and ("Fix" not in tmpList):
            continue
        if whole_tds[0].get_text() not in result.keys():
            result[whole_tds[0].get_text()] = [whole_tds[1].get_text()]
        else:
            result[whole_tds[0].get_text()].append(whole_tds[1].get_text())

row = 0
column = 0

workbook = xlsxwriter.Workbook('log4J_Vulnerabilities.xlsx')
bold = workbook.add_format({'bold': True})
header_list = list(result.keys())
worksheet = workbook.add_worksheet()
data_Format1 = workbook.add_format({'border': True, 'bold': True, 'bg_color': '#ff5e5e'})
data_Format2 = workbook.add_format({'border': True, 'bg_color': '#d9d9d9'})
data_Format3 = workbook.add_format({'border': True, 'bg_color': '#ffffff'})

for header in header_list:
    row = 0
    worksheet.write(row, column, header, data_Format1)
    vuln_list = list(result[header])
    for vulnerability in vuln_list:
        row += 1
        worksheet.write(row, column, vulnerability, data_Format2 if row % 2 == 0 else data_Format3)
    column += 1
workbook.close()
