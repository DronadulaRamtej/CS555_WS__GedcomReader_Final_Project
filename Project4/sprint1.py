"""
Name: Dronadula Ramtej
CWID: 20009102

Description: Use cases for checking the anomalies in a given gedcom file

Use cases tested: 
US01: Dates after current date
US02: Birth before marriage
US11: no bigamy
"""


import datetime

"""We use this function to create a new list for each individual"""
def individualList():
    l1 = [0] * 5
    l1.extend([[]])
    l1.extend([0] * 1)
    return l1


"""Here we print the contents of the list"""
def printListItems(l1):
    print('\n'.join(map(str, l1)))


def MarDateFromID(famList, id):
    matches = list(filter(lambda i: i[0] == id, famList))
    return matches[0][3] if matches else None


"""Here we create a new list for a new famiy using this function"""
def familyList():
    l1 = [0] * 5
    l1.extend([[]])
    l1.extend([0] * 1)
    return l1


"""This function  removes the slashes in .ged file"""
def returnLastName(s1):
    return s1.translate(str.maketrans('', '', '/'))





"""We return the curr date"""
def returnCurDate():
    curr_date = datetime.date.today()
    return str(curr_date.year) + '-' + str(curr_date.month).zfill(2) + '-' + str(curr_date.day).zfill(2)



"""Converts the date format from '2000 JUNE 12' to '2000-06-12'"""
def changeDateFormat(date):
    months = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
              'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    day, month, year = date.split()
    return f"{year}-{months[month]}-{day.zfill(2)}"




def returnBirthdayFromId(indiList, id):
    birth_dates = list(filter(lambda i: i[0] == id, indiList))
    return birth_dates[0][3] if birth_dates else None


def getSpouseByID(list_fam, fam_id, sp_id):
    return next((i[2] if i[1] == sp_id else i[1] for i in list_fam if i[0] == fam_id), None)

def BirthBeforeMarr(indiList, famList):
    bad_list = []
    i = 0
    while i < len(indiList):
        birth_date = indiList[i][3]
        if indiList[i][5] != []:
            j = 0
            while j < len(indiList[i][5]):
                if birth_date > MarDateFromID(famList, indiList[i][5][j]):
                    bad_list.append(indiList[i][0])
                    print("US02: The Individual " + indiList[i][0] + " has Birth Date occuring after his/her Marriage Date.")
                    break
                j += 1
        i += 1
    if not bad_list:
        print("US02: All the Individuals have their Birth Dates before their Marriage Dates.")
        print()
    else:
        print("US02: The following Individual(s) have their Birth Dates occuring before theirvMarriage Dates: ", end='')
        print(bad_list)
        print()


def getDeathDateByID(list_indi, id):
    filtered = filter(lambda indi: indi[0] == id and indi[4] != 0, list_indi)
    return next(filtered, None)[4]


def noBigamy(indiList, famList):
    bad_list = [i[0] for i in indiList if len(i[5]) > 1 and any(MarDateFromID(famList, j) < divDatefromID(famList, j) or MarDateFromID(famList, j) < getDeathDateByID(indiList, getSpouseByID(famList, j, i[0])) for j in i[5])]
    if len(bad_list) == 0:
        print("US11: No Individual is involved in any kind of Bigamy.")
        print()
    else:
        print("US11: The following Individual(s) are involved in Bigamy: ", end = '')
        print(bad_list)
        print()


def DatesBeforeCurrDate(indiList, famList):
    curr_date = returnCurDate()
    bad_dates = []
    for i in indiList + famList:
        if i[3] and i[3] > curr_date:
            bad_dates.append(i[3])
            if i[0].startswith('I'):
                print(f"US01: The Birth Date {i[3]} of Individual {i[0]} occurs before the current date.")
            else:
                print(f"US01: The Marriage Date {i[3]} of Family {i[0]} occurs before the current date.")
        if i[4] and i[4] > curr_date:
            bad_dates.append(i[4])
            if i[0].startswith('I'):
                print(f"US01: The Death Date {i[4]} of Individual {i[0]} occurs before the current date.")
            else:
                print(f"US01: The Divorce Date {i[4]} of Family {i[0]} occurs before the current date.")
    if not bad_dates:
        print("US01: All Dates are before the current date.\n")
    else:
        print(f"US01: The following Date(s) occur before the current date: {bad_dates}\n")




def divDatefromID(list_fam, id):
    return next((fam[4] for fam in list_fam if fam[0] == id), None)



def getMarrAgeByID(indiList, id, marri_date):
    temp = marri_date.split('-')
    marr_year = int(temp[0])
    marr_month = int(temp[1])
    marr_date = int(temp[2])
    for i in indiList:
        if(i[0] == id):
            birth_date = i[3]
    temp = birth_date.split('-')
    birth_year = int(temp[0])
    birth_month = int(temp[1])
    birth_date = int(temp[2])
    return marr_year - birth_year - ((marr_month, marr_date) < (birth_month, birth_date))



def parse(file_name):
    f = open(file_name,'r')
    indi_on = 0
    fam_on = 0
    list_indi = []
    list_fam = []
    indi = individualList()
    fam = familyList()
    for line in f:
        str = line.split()
        if(str != []):
            if(str[0] == '0'):
                if(indi_on == 1):
                    list_indi.append(indi)
                    indi = individualList()
                    indi_on = 0
                if(fam_on == 1):
                    list_fam.append(fam)
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
                        indi[3] = changeDateFormat(date)
                    if(date_id == 'DEAT'):
                        indi[4] = changeDateFormat(date)
                    if(date_id == 'MARR'):
                        fam[3] = changeDateFormat(date)
                    if(date_id == 'DIV'):
                        fam[4] = changeDateFormat(date)
    return list_indi, list_fam

def main(file_name):
    indiList, famList = parse(file_name)
    indiList.sort()
    famList.sort()
    printListItems(indiList)
    printListItems(famList)
    noBigamy(indiList, famList)
    DatesBeforeCurrDate(indiList, famList)
    BirthBeforeMarr(indiList, famList)
    

main('gedcomTest.ged')