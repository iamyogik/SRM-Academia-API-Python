from pyquery import PyQuery as pq
import json
import requests

AttendanceDetails = {}


def get_attendancedata(index, element):
    CourseCode = pq(element).find('td').eq(0).text()

    if CourseCode.find("Regular") == -1:
        pass
    else:
        CourseCode = CourseCode[:-8]

        # print("NEW = " + CourseCode)
        AttendanceDetails[CourseCode] = {
            "CourseTitle": pq(element).find('td').eq(1).text(),
            "Category": pq(element).find('td').eq(2).text(),
            "FacultyName": pq(element).find('td').eq(3).text(),
            "Slot": pq(element).find('td').eq(4).text(),
            "RoomNo": pq(element).find('td').eq(5).text(),
            "HoursConducted": pq(element).find('td').eq(6).text(),
            "HoursAbsent": pq(element).find('td').eq(7).text(),
            "Attendance": pq(element).find('td').eq(8).text(),
            "UniversityPracticalDetails": pq(element).find('td').eq(9).text()}


Marks = {}


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

    Marks[CourseCode] = Marks_each
    Marks[CourseCode]["TOTAL"] = MarksTotal


url = "https://academia.srmuniv.ac.in/liveViewHeader.do"


def getAttendenceAndMarks(token):
    headers = {"Cookie": token,
               'Origin': 'https://academia.srmuniv.ac.in',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
               }
    data = {"sharedBy": "srm_university",
            "appLinkName": "academia-academic-services",
            "viewLinkName": "My_Attendance",
            "urlParams": {},
            "isPageLoad": "true"}

    dom = pq(requests.post(url, data=data, headers=headers).text)
    dom('table[border="1"]').eq(0).find('tr:nth-child(n + 2)').each(get_attendancedata)
    dom('table[align="center"]').eq(2).find('tr:nth-child(n + 2)').each(get_marks)


    AttendanceAndMarks = {}

    for index, value in AttendanceDetails.items():
        if index in Marks:
            value["Marks"] = Marks[index]
        else:
            value["Marks"] = "Not Updated Yet"
        AttendanceAndMarks[index] = value

    AttendanceAndMarks = json.dumps(AttendanceAndMarks)

    if len(AttendanceAndMarks) > 5:
        json_o = {"status": "success", "data": AttendanceAndMarks}
        json_o = json.dumps(json_o)
        return json_o
    else:
        json_o = {"status": "error", "msg": "Error in token"}
        json_o = json.dumps(json_o)
        return json_o
