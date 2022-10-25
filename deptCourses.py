import requests
import json
from functools import cmp_to_key
from datetime import datetime

##CISE dept code: 19140000
##ECE dept code: 19050000

nameCodes = {
    'ECE': '19050000',
    'CISE': '19140000',
    'spring': '1',
    'summer': '5',
    'fall': '8'
}

startMonths = [1, 5, 8]

semesterCodes = []
isLyndsey = False

bypass = input("Input codes to bypass, press Enter for instructions\n")
if bypass:
    if bypass.lower() == "lyndsey":    
        print("Hi Lyndsey! :)")
        isLyndsey = True
        
        searchLimit = datetime.now().month
        while searchLimit%12 not in startMonths:
            searchLimit += 1
        monthIndex = startMonths.index(searchLimit%12)
        year = datetime.now().year
        if searchLimit>12: year += 1
        semesterCodes.append(str(year)[0:1] + str(year)[2:] + str(searchLimit))
        for i in range(3):
            if monthIndex == 0:
                year -= 1
                monthIndex = 2
            else:
                monthIndex -= 1
            semesterCodes.append(str(year)[0:1] + str(year)[2:] + str(startMonths[monthIndex]))
        
        deptCodes = [nameCodes['ECE'], nameCodes['CISE']]

    elif bypass.lower() == "brayden":
        print("Hi Brayden! :)")
        isLyndsey = True
        
        searchLimit = datetime.now().month
        while searchLimit%12 not in startMonths:
            searchLimit += 1
        monthIndex = startMonths.index(searchLimit%12)
        year = datetime.now().year
        if searchLimit>12: year += 1
        semesterCodes.append(str(year)[0:1] + str(year)[2:] + str(searchLimit))
        for i in range(3):
            if monthIndex == 0:
                year -= 1
                monthIndex = 2
            else:
                monthIndex -= 1
            semesterCodes.append(str(year)[0:1] + str(year)[2:] + str(startMonths[monthIndex]))
        
        deptCodes = [nameCodes['CISE']]


    else:
        run = True
        semesterCodes.append(bypass)
        while run:
            code = input()
            if not code: break
            semesterCodes.append(code)


elif not isLyndsey:
    yearCode = input('What year would you like to search in? (Ex: "2022")\n')
    yearCode = yearCode[0:1] + yearCode[2:]

    semesterCode = input('What semester would you like to search in? (Ex: "spring" or "summer" or "fall")\n')
    semesterCodes.append(yearCode + nameCodes[semesterCode])

if not isLyndsey:
    deptCodes = []
    print('Type the department(s) you wish to search, "done" to end. (Ex: "ECE" or "CISE")')
    while True:
        code = input()
        if code == 'done': break
        deptCodes.append(nameCodes[code])
    ##semesterCode = "2221" #2 + last two digits of year + 1 for spring, 5 for summer, 8 for fall (start month)
    ##deptCodes = ['16140000', '16140300']
    ##deptCodes = ['19140000', '19050000']

res = []
totalCourses = 0

##print(semesterCodes, deptCodes)
for semesterCode in semesterCodes:
    for deptCode in deptCodes:
        print("Retrieving courses for semester " + semesterCode + " in department " + deptCode + "...")
        moreCourses = True
        retrievedCourses = 0
        lastCtrlNum = 0
        while moreCourses:
            cur = requests.get('https://one.ufl.edu/apix/soc/schedule/?category=CWSP&term=' + semesterCode + '&dept=' + deptCode + '&last-control-number=' + str(lastCtrlNum)).json()
            print("RETRIEVED ROWS: " + str(cur[0]["RETRIEVEDROWS"]))
            ##print("Retrieved: " + str(cur[0]["RETRIEVEDROWS"]) + "\tTotal: " + str(cur[0]["TOTALROWS"]))
            retrievedCourses += cur[0]["RETRIEVEDROWS"]
            ##print("retrievedCourses=" + str(retrievedCourses))
            if retrievedCourses == cur[0]["TOTALROWS"]: moreCourses = False
            lastCtrlNum = cur[0]["LASTCONTROLNUMBER"]
            res.append((cur, semesterCode))
            totalCourses += len(cur[0]["COURSES"])


class Course:
    def __init__(self, code, title, cred, prereq):
        self.code = code
        self.title = title
        self.cred = cred
        self.prereq = prereq
        self.instructors = [] #This is actually a list of tuples, the first element begin a Prof object, and the second being a year.
        #I didn't make the year a member of a Prof object so I could reference the same Prof for multiple semesters of teaching

class Prof:
    profList = {}
    
    def __init__(self, name, rating=None):
        self.name = name
        self.rating = rating
        if not rating:
            page = requests.get("http://ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=" + name + "&queryoption=TEACHER&queryBy=schoolId&sid=1100")
            response = json.loads(page.content)
            for prof in response['professors']:
                self.rating = prof['overall_rating'] #This will take last rating, works for no rating

courses = {}
courseNum = 1
print("Parsing course data and retrieving rateMyProfessor data...")
for responseTuple in res:
    response = responseTuple[0]
    semesterCode = responseTuple[1]
    for course in response[0]["COURSES"]:
        if courseNum%4==1: print(str(100*courseNum//totalCourses) + "%") ##Loading display
        if course["code"] + course["name"] not in courses: courses[course["code"] + course["name"]] = (Course(course["code"], course["name"], str(course["sections"][0]["credits"]), course["prerequisites"]))

        ##Adding professors
        instructorNames = []
        for section in course["sections"]: #Creating list of all professors that teach this class for the given semester
            for instructor in section['instructors']:
                if instructor['name'] not in instructorNames: instructorNames.append(instructor['name'])
                
        for profName in instructorNames: ##adding the professors to the course object and dictionary if necessary
            if profName in Prof.profList:
                courses[course["code"] + course["name"]].instructors.append((Prof.profList[profName], semesterCode)) #I'm adding the semester so I can show which semester a prof taught a class for large range searches
            else:
                newProf = Prof(profName)
                Prof.profList[profName] = newProf
                courses[course["code"] + course["name"]].instructors.append((newProf, semesterCode))

        courseNum += 1


def compareMaxRating(course0, course1): #Compare function used to sort classes by best professor rating
    course0Max = course1Max = 0
    for prof in [i[0] for i in course0.instructors]: #Gets only first element of each tuple
        try: #Lazy error proofing to fix the fact that ratings are str when scraped from ratemyprofessor
            if float(prof.rating)>course0Max: course0Max = float(prof.rating)
        except: pass
    for prof in [i[0] for i in course1.instructors]:
        try:
            if float(prof.rating)>course1Max: course1Max = float(prof.rating)
        except: pass
    return course1Max - course0Max #If returns <0, course0 has better rating, and will be put before other course

def compareAvgRating(course0, course1): #Compare function used to sort classes by average professor rating
    course0Avg = course1Avg = 0
    profs = 0
    for prof in [i[0] for i in course0.instructors]:
        try: #Lazy error proofing to fix the fact that ratings are str when scraped from ratemyprofessor
            course0Avg += float(prof.rating)
            profs += 1
        except: pass
    course0Avg /= profs
    profs = 0
    for prof in [i[0] for i in course1.instructors]:
        try:
            course1Avg += float(prof.rating)
            profs += 1
        except: pass
    course1Avg /= profs
    return course1Avg - course0Avg #If returns <0, course0 has better rating, and will be put before other course

def codeToSem(semCode):
    res = '20'
    res += semCode[1:3]
    if semCode[-1] == '1': res = "Spring of " + res
    elif semCode[-1] == '5': res = "Summer of " + res
    else: res = "Fall of " + res
    return res

for course in sorted(list(courses.values()), key=cmp_to_key(compareMaxRating))[::-1]: ##Reverse order so the best courses are most easily visible
##for course in courses:
    print(course.code)
    print(course.title)
    print(str(course.cred), "Credits")
    print("Prereq:" + course.prereq[7:])
    for prof in course.instructors:
        print(prof[0].name, prof[0].rating, codeToSem(prof[1]))
    print()
print("The courses are sorted in reverse order of best professor rating, the best rated are directly above")        
    
input("Press enter to close the program") # so .exe window doesn't close
