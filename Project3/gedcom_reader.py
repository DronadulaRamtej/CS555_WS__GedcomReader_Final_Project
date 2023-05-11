"""
Name: Dronadula Ramtej
CWID: 20009102

Description: This program reads a gedcom file and store the information of people and families in lists. Everyone on the family table 
are then printed in the console.

"""

from prettytable import PrettyTable as pt
import itertools as it
import datetime

def individual_table(list):
    header = ['Individual_ID','Name','Sex','Birth Date','Death Date', 'Spouse In', 'Child In']
    rows = [[i[0], i[1], i[2], i[3], i[4] if i[4] else 'NA', i[5] if i[5] else 'NA', i[6] if i[6] else 'NA'] for i in list]
    max_lengths = [max(len(str(row[i])) for row in rows) for i in range(len(header))]
    output = ""
    for row in [header] + rows:
        output += "|" + "|".join(str(row[i]).ljust(max_lengths[i]) for i in range(len(header))) + "|\n"
    print(output)

def family_table(list):
    header = ['Family_ID', 'Husband ID', 'Wife ID', 'Marriage Date', 'Divorce Date', 'Children']
    rows = [[i[0], i[1], i[2], i[3], i[4] if i[4] != 0 else 'NA', i[5] if i[5] != [] else 'NA'] for i in list]
    table = pt(header)
    for row in rows:
        table.add_row(row)
    print(table)



def indi_list():
    op_list = [0] * 5
    op_list.extend([[]])
    op_list.extend([0] * 1)
    return op_list


def dateConversion(date):
    months = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
              'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    day, month, year = date.split()
    return f"{year}-{months[month]}-{day.zfill(2)}"




def family_list():
    op_list = [0] * 5
    op_list.extend([[]])
    op_list.extend([0] * 1)
    return op_list


def Last_Name(s):
    return s.translate(str.maketrans('', '', '/'))


def parse(filename):
    f = open(filename,'r')
    indi_on = 0
    fam_on = 0
    list_indi = []
    list_fam = []
    indi = indi_list()
    fam = family_list()
    for line in f:
        str = line.split()
        if(str != []):
            if(str[0] == '0'):
                if(indi_on == 1):
                    list_indi.append(indi)
                    indi = indi_list()
                    indi_on = 0
                if(fam_on == 1):
                    list_fam.append(fam)
                    fam = family_list()
                    fam_on = 0
                if(str[1] in ['NOTE', 'HEAD', 'TRLR']):
                    pass
                else:
                    if(str[2] == 'INDI'):
                        indi_on = 1
                        indi[0] = (str[1])
                    if(str[2] == 'FAM'):
                        fam_on = 1
                        fam[0] = (str[1])
            if(str[0] == '1'):
                if(str[1] == 'NAME'):
                    indi[1] = str[2] + " " + Last_Name(str[3])
                if(str[1] == 'SEX'):
                    indi[2] = str[2]
                if(str[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']):
                    date_id = str[1]
                if(str[1] == 'FAMS'):
                    indi[5].append(str[2])
                if(str[1] == 'FAMC'):
                    indi[6] = str[2]
                if(str[1] == 'HUSB'):
                    fam[1] = str[2]
                if(str[1] == 'WIFE'):
                    fam[2] = str[2]
                if(str[1] == 'CHIL'):
                    fam[5].append(str[2])
            if(str[0] == '2'):
                if(str[1] == 'DATE'):
                    date = str[4] + " " + str[3] + " " + str[2]
                    if(date_id == 'BIRT'):
                        indi[3] = dateConversion(date)
                    if(date_id == 'DEAT'):
                        indi[4] = dateConversion(date)
                    if(date_id == 'MARR'):
                        fam[3] = dateConversion(date)
                    if(date_id == 'DIV'):
                        fam[4] = dateConversion(date)
    return list_indi, list_fam




def main(file_name):
    list_indi, list_fam = parse(file_name)
    list_indi.sort()
    list_fam.sort()

    individual_table(list_indi)
    family_table(list_fam)

main('gedcomTest.ged')