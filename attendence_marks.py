from pyquery import PyQuery as pq
import json
import requests
import base64
import re


AttendanceDetails = []

def getCookieFromToken(token):
    try:
        token = token.replace('\\n', '\n')
        token = base64.decodestring(str.encode(token))
        cookie = json.loads(token)
        return cookie
    except:
        return "error"





def get_attendancedata(index, element):
    CourseCode = pq(element).find('td').eq(0).text()

    if CourseCode.find("Regular") == -1:
        pass
    else:
        CourseCode = CourseCode[:-8]


        AttendanceDetails.append({
            "CourseCode": CourseCode,
            "CourseTitle": pq(element).find('td').eq(1).text(),
            "Category": pq(element).find('td').eq(2).text(),
            "FacultyName": pq(element).find('td').eq(3).text(),
            "Slot": pq(element).find('td').eq(4).text(),
            "RoomNo": pq(element).find('td').eq(5).text(),
            "HoursConducted": pq(element).find('td').eq(6).text(),
            "HoursAbsent": pq(element).find('td').eq(7).text(),
            "Attendance": pq(element).find('td').eq(8).text(),
            "UniversityPracticalDetails": pq(element).find('td').eq(9).text()})


Marks = []


def get_marks(index, element):
    CourseCode = pq(element).find('td').eq(0).text()
    Marks_each = {}
    MarksTotal = 0
    for a in pq(element).find('td').eq(2).find('td'):
        testLabel = pq(a).find('strong').text()
        testLabelAndMarks = pq(a).text()
        testMarks = testLabelAndMarks.replace(testLabel, '')
        testMarks = testMarks.replace(" ", "")
        Marks_each[testLabel] = testMarks
        if (testMarks == "Abs"):
            continue
        else:
            MarksTotal = MarksTotal + float(testMarks)

    Marks_each["CourseCode"] = CourseCode;
    Marks_each["Total"] = MarksTotal;

    Marks.append(Marks_each)


url = "https://academia.srmuniv.ac.in/liveViewHeader.do"


def getAttendenceAndMarks(token):


    Cookies = getCookieFromToken(token)
    if (Cookies == "error"):
        json_o = {"status": "error", "msg": "Error in token"}
        json_o = json.dumps(json_o)
        return json_o
    else:

        viewLinkName = "My_Attendance"

        headers = {'Origin': 'https://academia.srmuniv.ac.in',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
                   }
        data = {"sharedBy": "srm_university",
                "appLinkName": "academia-academic-services",
                "viewLinkName": viewLinkName,
                "urlParams": {},
                "isPageLoad": "true"}

        dom = requests.post(url, data=data, headers=headers, cookies=Cookies).text

        s1 = '$("#zc-viewcontainer_'+viewLinkName+'").prepend(pageSanitizer.sanitize('
        s2 = '});</script>'
        a, b = dom.find(s1), dom.find(s2)
        dom = pq(dom[a + 56 + len(viewLinkName):b - 5])


        dom('table[border="1"]').eq(0).find('tr:nth-child(n + 2)').each(get_attendancedata)
        dom('table[align="center"]').eq(2).find('tr:nth-child(n + 2)').each(get_marks)


        AttendanceAndMarks = []

        for value_att in AttendanceDetails:

            for value_marks in Marks:

                if value_att["CourseCode"] == value_marks["CourseCode"]:
                    req_marks = value_marks.copy()
                    req_marks.pop('CourseCode', None)
                    value_att["Marks"] = req_marks
                else:
                    continue
            AttendanceAndMarks.append(value_att)


        if len(AttendanceAndMarks) > 5:
            json_o = {"status": "success", "data": AttendanceAndMarks}
            json_o = json.dumps(json_o)
            return json_o
        else:
            json_o = {"status": "error", "msg": "Error occured"}
            json_o = json.dumps(json_o)
            return json_o




