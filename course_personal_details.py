from pyquery import PyQuery as pq
import json
import requests
import base64

CourseDetails = {}
FacultyAdvisors = []


def getCookieFromToken(token):
    try:
        token = token.replace('\\n', '\n')
        token = base64.decodestring(str.encode(token))
        cookie = json.loads(token)
        return cookie
    except:
        return "error"





def get_CourseDetails(index, element):
    CourseCode = pq(element).find("td").eq(0).text()
    CourseDetails[CourseCode] = {"CourseCode": pq(element).find("td").eq(0).text(),
                          "CourseTitle": pq(element).find("td").eq(1).text(),
                          "RegnType": pq(element).find("td").eq(2).text(),
                          "Category": pq(element).find("td").eq(3).text(),
                          "CourseType": pq(element).find("td").eq(4).text(),
                          "FacultyName": pq(element).find("td").eq(5).text(),
                          "Slot": pq(element).find("td").eq(6).text(),
                          "RoomNo": pq(element).find("td").eq(7).text() }



def get_facultyadvisordetails(index, element):
    FacultyAdvisors_each = {"FacultyAdvisorName": pq(element).find("strong").eq(0).text(),
                       "FacultyAdvisorEmail": pq(element).find("font").eq(0).text()}
    FacultyAdvisors.append(FacultyAdvisors_each)


def get_personaldetails(dom):
    RegistrationNumber = dom('table[cellspacing="1"]').eq(0).find('td').eq(1).text()
    Name = dom('table[cellspacing="1"]').eq(0).find('td').eq(3).text()
    Batch = dom('table[cellspacing="1"]').eq(0).find('td').eq(5).text()
    Mobile = dom('table[cellspacing="1"]').eq(0).find('td').eq(7).text()
    Program = dom('table[cellspacing="1"]').eq(0).find('td').eq(9).text()
    Department = dom('table[cellspacing="1"]').eq(0).find('td').eq(11).text()
    Semester = dom('table[cellspacing="1"]').eq(0).find('td').eq(13).text()

    PersonalDetails = { "RegistrationNumber": RegistrationNumber,
                       "Name": Name,
                       "Batch": Batch,
                       "Mobile": Mobile,
                       "Program": Program,
                       "Department": Department,
                       "Semester": Semester }
    return PersonalDetails





url = "https://academia.srmuniv.ac.in/liveViewHeader.do"

def getCoursePersonalDetailsData(token,sem="ODD"):
    if(sem == "EVEN"):
        viewLinkName = "My_Time_Table_2017_18_EVEN"
    elif(sem == "ODD"):
        viewLinkName = "My_Time_Table_2017_18_ODD"
    else:
        json_o = {"status": "error", "msg": "Error in batch name."}
        json_o = json.dumps(json_o)
        return json_o

    Cookies = getCookieFromToken(token)
    if(Cookies=="error"):
        json_o = {"status": "error", "msg": "Error in token"}
        json_o = json.dumps(json_o)
        return json_o
    else:


        headers = {'Origin': 'https://academia.srmuniv.ac.in',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
                   }
        data = {"sharedBy": "srm_university",
                "appLinkName": "academia-academic-services",
                "viewLinkName": viewLinkName,
                "urlParams": {},
                "isPageLoad": "true"}

        dom = pq(requests.post(url, data=data, headers=headers, cookies=Cookies).text)
        dom('table[border="1"]').find('tr:nth-child(n + 2)').each(get_CourseDetails)
        dom('td[align="center"]').each(get_facultyadvisordetails)


        PersonalDetails = get_personaldetails(dom)

        CompleteDetails = {}

        CompleteDetails['PersonalDetails'] = PersonalDetails
        CompleteDetails['FacultyAdvisors'] = FacultyAdvisors
        CompleteDetails['CourseDetails'] = CourseDetails
        return CompleteDetails


def getCoursePersonalDetails(token):
    CompleteDetails = getCoursePersonalDetailsData(token, "EVEN")
    if len(CompleteDetails['PersonalDetails']['RegistrationNumber']) > 5:
        json_o = {"status": "success", "data": CompleteDetails}
        print(11111)
        json_o = json.dumps(json_o)
        return json_o
    else:
        CompleteDetails2 = getCoursePersonalDetailsData(token, "ODD")

        if len(CompleteDetails2['PersonalDetails']['RegistrationNumber']) > 5:
            json_o = {"status": "success", "data": CompleteDetails2}
            json_o = json.dumps(json_o)
            return json_o
        else:
            json_o = {"status": "error", "msg": "Error in token"}
            json_o = json.dumps(json_o)
            return json_o

    
