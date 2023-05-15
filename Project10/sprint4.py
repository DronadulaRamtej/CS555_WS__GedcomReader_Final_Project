
"""
Name: Dronadula Ramtej
CWID: 20009102

Description: Use cases for checking the anomalies in a given gedcom file

Use cases tested: 
US14: Multiple births <= 5
US04: Marriage before divorce
US29: List deceased
US12: Parents not too old
US05: Marriage before death0
US30: List living married
US09: Birth before death of parents
"""

from prettytable import PrettyTable as pt
import datetime


"""We use this function to create a new list for each individual"""
def indiList():
    op_list = [0] * 5
    op_list.extend([[]])
    op_list.extend([0] * 1)
    return op_list



def individualTable(l1):
    header = ['Individual_ID','Name','Sex','Birth Date','Death Date', 'Spouse In', 'Child In']
    rows = [[i[0], i[1], i[2], i[3], i[4] if i[4] else 'NA', i[5] if i[5] else 'NA', i[6] if i[6] else 'NA'] for i in l1]
    max_lengths = [max(len(str(row[i])) for row in rows) for i in range(len(header))]
    output = ""
    for row in [header] + rows:
        output += "|" + "|".join(str(row[i]).ljust(max_lengths[i]) for i in range(len(header))) + "|\n"
    print(output)



"""Here we create a new list for a new famiy using this function"""
def famList():
    op_list = [0] * 5
    op_list.extend([[]])
    op_list.extend([0] * 1)
    return op_list



def returnLastName(s):
    return s[1:-1]



def familyTable(l1):
    header = ['Family_ID', 'Husband ID', 'Wife ID', 'Marriage Date', 'Divorce Date', 'Children']
    rows = [[i[0], i[1], i[2], i[3], i[4] if i[4] != 0 else 'NA', i[5] if i[5] != [] else 'NA'] for i in l1]
    table = pt(header)
    for row in rows:
        table.add_row(row)
    print(table)


def returnCurDate():
    curr_date = datetime.date.today()
    return str(curr_date.year) + '-' + str(curr_date.month).zfill(2) + '-' + str(curr_date.day).zfill(2)

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


def birthBeforeDeathOfParents(indiList, famiList):
    bad_data_list = []
    for i in famiList:
        if(i[5] != []):
            for j in i[5]:
                child_birth_date = birthById(indiList, j)
                if(deathById(indiList, i[2]) != None):
                    mother_death_date = deathById(indiList, i[2])
                    if(child_birth_date > mother_death_date):
                        bad_data_list.append(j)
                        print("US09: The child " + j + " was born after the death of his/her mother " + i[2] + ".")
                if(deathById(indiList, i[1]) != None):
                    father_month_diff = monthsGap(child_birth_date, deathById(indiList, i[1]))
                    if(father_month_diff > 9):
                        bad_data_list.append(j)
                        print("US09: The child " + j + " was born 9 months after the death of his/her father " + i[1] + ".")
    if(len(bad_data_list) == 0):
        print("US09: All children were born before their parents died, and there were no mistakes in the statistics.")
        print()
    else:
        print("US09: The birth dates of the following children are wrong based on when their parents died: ", end = '')
        print(bad_data_list)
        print()



def deathById(indiList, id):
    matches = list(filter(lambda x: x[0] == id, indiList))
    for i in matches:
        if i[4] != 0:
            return i[4]

def ParNotOld(indiList, famiList):
    bad_data_list = [i[2] for i in famiList if i[5] and returnAgeFromID(indiList, i[2]) - min([returnAgeFromID(indiList, j) for j in i[5]]) >= 60]
    bad_data_list += [i[1] for i in famiList if i[5] and returnAgeFromID(indiList, i[1]) - min([returnAgeFromID(indiList, j) for j in i[5]]) >= 80]
    if len(bad_data_list) == 0:
        print("US12: No one is too old to be a parent.")
    else:
        print("US12: The parents of the following children are too old for them: ", end='')
        print(bad_data_list)
    print()

def ListDeceased(indiList):
    """ US29 - Here the list the deceased individuals """
    deceased = [i for i in indiList if i[4] != 0]
    print(f"US29: Here's the list of Deceased individuals is : {[i[0] for i in deceased]}")
    for i in deceased:
        print(f"{i[0]}: Individual {retNameById(indiList, i[0])} passed away on {deathById(indiList, i[0])}")
    print()


def returnAgeFromID(indiList, id):
    dead_flag = 0
    for i in indiList:
        if(i[0] == id):
            birth_date = i[3]
            if(i[4] != 0):
                death_date = i[4]
                dead_flag = 1
    temp = birth_date.split('-')
    birth_year = int(temp[0])
    birth_month = int(temp[1])
    birth_date = int(temp[2])
    if(dead_flag == 1):
        temp = death_date.split('-')
        death_year = int(temp[0])
        death_month = int(temp[1])
        death_date = int(temp[2])
        return death_year - birth_year - ((death_month, death_date) < (birth_month, birth_date))
    curr_date = returnCurDate().split('-')
    curr_year = int(curr_date[0])
    curr_month = int(curr_date[1])
    curr_date = int(curr_date[2])
    return curr_year - birth_year - ((curr_month, curr_date) < (birth_month, birth_date))



def marriBeforeDivorce(famiList):
    bad_list = list(filter(lambda i: i[4] != 0 and i[3] > i[4], famiList))
    if len(bad_list) > 0:
        print("US04: The marriage dates of the following family(s) come after their divorce dates: ", end='')
        print([i[0] for i in bad_list])
        print()
    else:
        print("US04: All of the families' dates of marriage come before their dates of divorce.")
        print()




def retNameById(indiList, id):
    return [i[1] for i in indiList if i[0] == id][0]


def ListLivMarri(indiList, famiList):
    spouse_ids = set(filter(lambda x: deathById(indiList, x) is None, [i[1] for i in famiList] + [i[2] for i in famiList]))
    print("US30: List of Living Married Individuals", list(spouse_ids))
    for i in spouse_ids:
        print(i + ": Individual " + retNameById(indiList, i) + " is married and belongs to family " + str(returnSpNameFromId(indiList, i)))
    print()


def marriBeforeDeath(famiList, indiList):
    bad_list = []
    for i in famiList:
        if any(deathById(indiList, s) != None and i[3] > deathById(indiList, s) for s in [i[1], i[2]]):
            bad_list.append(i[0])
            print(f"US05: The Family {i[0]} has Marriage date after the Death date of one of the Spouses.")
    if len(bad_list) == 0:
        print("US05: All of the families' marriage dates are before their spouses' death dates.")
        print()
    else:
        print("US05: The weddings of the following families happened after the death of one of the spouses: ", end='')
        print(bad_list)
        print()



def returnSpNameFromId(indiList, id):
    indi_info = list(filter(lambda x: x[0] == id, indiList))
    return indi_info[0][5] if indi_info else None

def multipleBir(indiList, famiList):
    bad_data_list = []
    for fam in famiList:
        if len(fam[5]) > 5:
            sibling_birth_dates = [birthById(indiList, sid) for sid in fam[5]]
            for bd in set(sibling_birth_dates):
                if sibling_birth_dates.count(bd) > 4:
                    bad_data_list.append(fam[0])
                    print(f"US14: The Family {fam[0]} has had more than 5 births on {bd}, which is invalid.")
    if len(bad_data_list) == 0:
        print("US14:All families have had no more than five kids at a time when they were born.")
        print()
    else:
        print("US14: The following families have had more than 5 kids at once: ", end='')
        print(bad_data_list)
        print()



def monthsGap(d1, d2):
    year1, month1, day1 = map(int, d1.split('-'))
    year2, month2, day2 = map(int, d2.split('-'))
    years, months = divmod(year1 - year2, 12)
    months += (month1 - month2)
    if day1 < day2:
        months -= 1
    return years * 12 + months



def parse(file_name):
    f = open(file_name,'r')
    indi_on = 0
    fam_on = 0
    indi_list = []
    famiList = []
    indi = indiList()
    fam = famList()
    for line in f:
        str = line.split()
        if(str != []):
            if(str[0] == '0'):
                if(indi_on == 1):
                    indi_list.append(indi)
                    indi = indiList()
                    indi_on = 0
                if(fam_on == 1):
                    famiList.append(fam)
                    fam = famList()
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
    return indi_list, famiList

def main(file_name):
    indi_list, famiList = parse(file_name)
    indi_list.sort()
    famiList.sort()
    
    individualTable(indi_list)
    familyTable(famiList)
    

    multipleBir(indi_list,famiList)
    marriBeforeDivorce(famiList)
    ListDeceased(indi_list)
    ParNotOld(indi_list, famiList)
    ListLivMarri(indi_list, famiList)
    marriBeforeDeath(famiList, indi_list)
    birthBeforeDeathOfParents(indi_list, famiList)
    
    
    

main('gedcomTest.ged')