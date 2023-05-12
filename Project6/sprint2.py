"""
Name: Dronadula Ramtej
CWID: 20009102

Description: Use cases for checking the anomalies in a given gedcom file

Use cases tested: 
US21: Correct gender for role
US22: Unique IDs
US10: Marriage after 14
"""
import datetime

"""We use this function to create a new list for each individual"""
def individualList():
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


"""Here we create a new list for a new famiy using this function"""
def familyList():
    l1 = [0] * 5
    l1.extend([[]])
    l1.extend([0] * 1)
    return l1


"""Converts the date format from '2000 JUNE 12' to '2000-06-12'"""
def changeDateFormat(date):
    months = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
              'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    day, month, year = date.split()
    return f"{year}-{months[month]}-{day.zfill(2)}"


"""Here we print the contents of the list"""
def printListItems(l1):
    print('\n'.join(map(str, l1)))


def Marriage_Before_14(indiList, famiList):
    bad_list = []
    i = 0
    while i < len(famiList):
        if MarriAgeFromId(indiList, famiList[i][1], famiList[i][3]) < 14:
            bad_list.append(famiList[i][1])
            print("US10: The Individual " + famiList[i][1] + " married before turning 14 years of age in family " + famiList[i][0] + ".")
        if MarriAgeFromId(indiList, famiList[i][2], famiList[i][3]) < 14:
            bad_list.append(famiList[i][2])
            print("US10: The Individual " + famiList[i][2] + " married before turning 14 years of age in family " + famiList[i][0] + ".")
        i += 1

    if not bad_list:
        print("US10: No Individual married before turning 14 years of age.")
        print()
    else:
        print("US10: The following Individual(s)  are married before turning 14 years of age: ", end='')
        print(bad_list)
        print()


def MarriAgeFromId(indiList, id, marridate):
    temp = marridate.split('-')
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



def CorrectGenderForRole(indiList, famiList):
    bad_list = []
    for i in famiList:
        if(sexFromID(indiList, i[1]) != 'M'):
            bad_list.append(i[1])
            print("US21: The Individual " + i[1] + " in family " + i[0] + " has incorrect Gender role.")
        if(sexFromID(indiList, i[2]) != 'F'):
            bad_list.append(i[2])
            print("US21: The Individual " + i[2] + " in family " + i[0] + " has incorrect Gender role.")
    if(len(bad_list) == 0):
        print("US21: The Individuals in all the Families have incorrect gender roles.")
        print()
    else:
        print("US21: The following Individual(s) have incorrect gender role: ", end = '')
        print(bad_list)
        print()

def sexFromID(indiList, id):
    for i in indiList:
        if(i[0] == id):
            return i[2]

def UniqueIDs(indiList, famiList):
    indi_id_list = []
    fam_id_list = []
    dup_iid_list = []
    dup_fid_list = []
    flag = 0
    for i in indiList:
        indi_id_list.append(i[0])
    for i in famiList:
        fam_id_list.append(i[0])
    if(len(indi_id_list) == len(set(indi_id_list)) and len(fam_id_list) == len(set(fam_id_list))):
        print("\nUS22: All the IDs are unique.")
        print()
    else:
        for i in indi_id_list:
            flag = 0
            for j in indi_id_list:
                if (i == j):
                    flag += 1
                    if(flag > 1):
                        dup_iid_list.append(i)
        for i in fam_id_list:
            flag = 0
            for j in fam_id_list:
                if (i == j):
                    flag += 1
                    if(flag > 1):
                        dup_fid_list.append(i)
        if(len(dup_iid_list) != 0):
            print("\nUS22: The following Individual ID(s) have same ID's: ", end = '')
            print(set(dup_iid_list))
            print()
        if(len(dup_fid_list) != 0):
            print("US22: The following Family ID(s) have same ID's: ", end = '')
            print(set(dup_fid_list))
            print()

def parse(file_name):
    f = open(file_name,'r')
    indi_on = 0
    fam_on = 0
    indiList = []
    famiList = []
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
                    famiList.append(fam)
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
    return indiList, famiList

def main(file_name):
    list_indi, list_fam = parse(file_name)
    list_indi.sort()
    list_fam.sort()
    printListItems(list_indi)
    printListItems(list_fam)

    UniqueIDs(list_indi, list_fam)
    CorrectGenderForRole(list_indi, list_fam)
    Marriage_Before_14(list_indi, list_fam)
    

main('gedcomTest.ged')


