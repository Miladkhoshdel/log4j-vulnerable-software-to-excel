# made with love by Milad Khoshdel for personal use
# https://regux.com
# Edited by Mehdi Bastani

import requests
from bs4 import BeautifulSoup
import xlsxwriter

page = requests.get("https://github.com/NCSC-NL/log4shell/blob/main/software/README.md")
soup = BeautifulSoup(page.content, 'html.parser')

all_tables = soup.find_all('table')
result = {}

# Remove redundant tables
all_tables = list(filter(lambda st: "Supplier" in st.find("thead").get_text(), all_tables))

for table in all_tables:
    whole_table = table.find('tbody')
    rows = whole_table.find_all('tr')
    for tr in rows:
        whole_tds = tr.find_all('td')
        if "Not" in whole_tds[3].get_text():
            continue
        if whole_tds[0].get_text() not in result.keys():
            result[whole_tds[0].get_text()] = [whole_tds[1].get_text()]
        else:
            result[whole_tds[0].get_text()].append(whole_tds[1].get_text())

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
        row += 1
        worksheet.write(row, column, vulnerability)
    column += 1
workbook.close()
