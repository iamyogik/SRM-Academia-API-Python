from flask import Flask
from flask import request as rq
import token_srm
import attendence_marks
import timetable
import course_personal_details
import json

app = Flask(__name__)


@app.route('/')
def home():
    json_o = {"status": "success", "msg": "Its working. *** ACADEMIA API WITH PYTHON *** By Yogesh Kumawat"}
    json_o = json.dumps(json_o)
    return json_o



@app.route('/token', methods=['GET', 'POST'])
def request():
    if 'email' in rq.args and 'pass' in rq.args:
        return token_srm.getToken(rq.args.get('email'), rq.args.get('pass'))
    else:
        json_o = {"status":"error", "msg":"Error in Input Parameters"}
        json_o = json.dumps(json_o)
        return json_o



@app.route('/AttAndMarks', methods=['GET', 'POST'])
def AttAndMarks():
    if 'token' in rq.args:
        token = rq.args.get('token')
        att_marks = attendence_marks.getAttendenceAndMarks(token)
        return att_marks
    else:
        json_o = {"status": "error", "msg": "Error in Input Parameters"}
        json_o = json.dumps(json_o)
        return json_o



@app.route('/TimeTable', methods=['GET', 'POST'])
def TimeTable():
    if 'batch' in rq.args and 'token' in rq.args:
        batchNo = rq.args.get('batch')
        token = rq.args.get('token')
        timeTable = timetable.getTimeTable(token, batchNo)
        return timeTable
    else:
        json_o = {"status": "error", "msg": "Error in Input Parameters"}
        json_o = json.dumps(json_o)
        return json_o



@app.route('/PersonalDetails', methods=['GET', 'POST'])
def getPersonalDetails():
    if 'sem' in rq.args and 'token' in rq.args:
        sem = rq.args.get('sem')
        token = rq.args.get('token')
        details = course_personal_details.getCoursePersonalDetails(token, sem)
        return details
    else:
        json_o = {"status": "error", "msg": "Error in Input Parameters"}
        json_o = json.dumps(json_o)
        return json_o





if __name__ == '__main__':
    app.run(debug=True)
