
"""
Name: Dronadula Ramtej
CWID: 20009102

Description: Use cases for checking the anomalies in a given gedcom file

Use cases tested: 
US06: Divorce before death
US13: Siblings spacing
US23: Unique name and birth date
US24: Unique families by spouses
"""

import datetime
import itertools as it
from prettytable import PrettyTable as pt





def individualTable(l1):
    header = ['Individual_ID','Name','Sex','Birth Date','Death Date', 'Spouse In', 'Child In']
    rows = [[i[0], i[1], i[2], i[3], i[4] if i[4] else 'NA', i[5] if i[5] else 'NA', i[6] if i[6] else 'NA'] for i in l1]
    max_lengths = [max(len(str(row[i])) for row in rows) for i in range(len(header))]
    output = ""
    for row in [header] + rows:
        output += "|" + "|".join(str(row[i]).ljust(max_lengths[i]) for i in range(len(header))) + "|\n"
    print(output)


def familyList():
    op_list = [0] * 5
    op_list.extend([[]])
    op_list.extend([0] * 1)
    return op_list

def familyTable(l1):
    header = ['Family_ID', 'Husband ID', 'Wife ID', 'Marriage Date', 'Divorce Date', 'Children']
    rows = [[i[0], i[1], i[2], i[3], i[4] if i[4] != 0 else 'NA', i[5] if i[5] != [] else 'NA'] for i in l1]
    table = pt(header)
    for row in rows:
        table.add_row(row)
    print(table)


def returnLastName(s):
    return s[1:-1]

def individualList():
    op_list = [0] * 5
    op_list.extend([[]])
    op_list.extend([0] * 1)
    return op_list

def dateFormatConversion(date):
    temp = date.split()
    month = {
        'JAN': '01',
        'FEB': '02',
        'MAR': '03',
        'APR': '04',
        'MAY': '05',
        'JUN': '06',
        'JUL': '07',
        'AUG': '08',
        'SEP': '09',
        'OCT': '10',
        'NOV': '11',
        'DEC': '12'
    }
    temp[1] = month.get(temp[1], temp[1])
    if(temp[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
        temp[2] = '0' + temp[2]
    return (temp[0] + '-' + temp[1] + '-' + temp[2])


def birthById(indiList, id):
    birth_dates = list(filter(lambda i: i[0] == id, indiList))
    return birth_dates[0][3] if birth_dates else None


def deathById(indiList, id):
    matches = list(filter(lambda x: x[0] == id, indiList))
    for i in matches:
        if i[4] != 0:
            return i[4]


def returnNamebyID(indiList, id):
    return [i[1] for i in indiList if i[0] == id][0]


def monthsGap(d1, d2):
    year1, month1, day1 = map(int, d1.split('-'))
    year2, month2, day2 = map(int, d2.split('-'))
    years, months = divmod(year1 - year2, 12)
    months += (month1 - month2)
    if day1 < day2:
        months -= 1
    return years * 12 + months


def daysGap(d1, d2):
    dt1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
    dt2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
    return abs((dt1 - dt2).days)




def DivoreBeforeDeath(famList, indiList):
    bad_list = [fam[0] for fam in famList if fam[4] != 0 and any(deathById(indiList, id_) is not None and fam[4] > deathById(indiList, id_) for id_ in (fam[1], fam[2]))]
    if not bad_list:
        print("US06: All marriages end before the death of either of the partners.")
    else:
        print(f"US06: The divorce dates of the following families are after the death of one of the partners.: {bad_list}")


def SibGap(s1, s2, indiList):
    diff_siblings_months = abs(monthsGap(birthById(indiList, s1), birthById(indiList, s2)))
    diff_siblings_days = abs(daysGap(birthById(indiList, s1), birthById(indiList, s2)))
    if(diff_siblings_months <= 8 and diff_siblings_days >= 3):
        return True, "Less than or equal to 8 months between birth dates"
    elif(diff_siblings_months == 0 and diff_siblings_days >= 2):
        return True, "More than or equal to 2 days between birth dates"
    else:
        return False, ""

def SiblingsSpacings(famList, indiList):
    bad_data_list = []
    for i in famList:
        if(i[5] != [] and len(i[5]) > 1):
            sibling_comb = list(it.combinations(i[5], 2))
            for j in sibling_comb:
                isBad, reason = SibGap(j[0], j[1], indiList)
                if(isBad):
                    bad_data_list.append((j[0], j[1], i[0], reason))
                    print("US13: Siblings " + j[0] + " and " + j[1] + " in Family " + i[0] + " have " + reason + ".")
    if(len(bad_data_list)==0):
        print("US13: All siblings in all families have the right amount of time between their birth dates.")
        print()
    else:
        print("US13: What follows Birth dates are too close together for sibling pairs in Families: ", end = '')
        print(bad_data_list)
        print()



def sameBirdateAndName(indiList):
    test_list = [(i[1], i[3]) for i in indiList]
    if(len(test_list) == len(set(test_list))):
        print("US23: Taking name and birth date into account, each person is unique.")
        print()
    else:
        bad_list = set([i for i in test_list if test_list.count(i) > 1])
        if(len(bad_list) != 0):
            print("US23: Duplicate names and birth dates have been found for the following people:", end = '')
            print(bad_list)
            print()


def sameSpousesFamilies(indiList, famList):
    test_set = {((returnNamebyID(indiList, i[1]), returnNamebyID(indiList, i[2]), i[3])) for i in famList}
    if len(test_set) == len(set(test_set)):
        print("US24: Based on the names of the spouses and the date they got married, every family is different.")
        print()
    else:
        bad_set = {i for i in test_set if test_set.count(i) > 1}
        if bad_set:
            print("US24: There are two of each of the following families, based on the names of the spouses and the dates they got married: ", end='')
            print(bad_set)
            print()


def parse(file_name):
    f = open(file_name,'r')
    indi_on = 0
    fam_on = 0
    indiList = []
    famList = []
    indi = individualList()
    fam = familyList()
    for line in f:
        str = line.split()
        if(str != []):
            if(str[0] == '0'):
                if(indi_on == 1):
                    indiList.append(indi)
                    indi = individualList()
                    indi_on = 0
                if(fam_on == 1):
                    famList.append(fam)
                    fam = familyList()
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
                    indi[1] = str[2] + " " + returnLastName(str[3])
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
                        indi[3] = dateFormatConversion(date)
                    if(date_id == 'DEAT'):
                        indi[4] = dateFormatConversion(date)
                    if(date_id == 'MARR'):
                        fam[3] = dateFormatConversion(date)
                    if(date_id == 'DIV'):
                        fam[4] = dateFormatConversion(date)
    return indiList, famList

def main(file_name):
    indiList, famList = parse(file_name)
    indiList.sort()
    famList.sort()
    
    individualTable(indiList)
    familyTable(famList)
    
    
    sameSpousesFamilies(indiList, famList)
    sameBirdateAndName(indiList)
    DivoreBeforeDeath(famList, indiList)
    SiblingsSpacings(famList, indiList)
    
    

main('gedcomTest.ged')