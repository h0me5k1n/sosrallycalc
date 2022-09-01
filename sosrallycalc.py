from flask import Flask, render_template, json, request, redirect
from threading import Thread
import datetime as dt
import time
from datetime import datetime, timedelta

rallymanager = Flask(__name__)
rallymanager.debug = True
jsnfile = 'rallyleads.json'

def run():
    rallymanager.run(host="0.0.0.0", port=3000)

@rallymanager.route("/")
def main():
    with open(jsnfile) as rr:
        rallies = json.load(rr)
    return render_template("rallyleadlist.html", rallies = rallies)
@rallymanager.route("/refresh", methods = ['GET'])
def refresh():
    return redirect('/')
@rallymanager.route("/addrallylead", methods = ['GET','POST'])
def addrallylead():
    if request.method == 'GET':
        return render_template("addrallylead.html", rally = {})
    if request.method == 'POST':
        id = request.form["playername"] + "-" + request.form["rallytarget"]
        #id = request.form["playername"]
        playername = request.form["playername"]
        rallytarget = request.form["rallytarget"]
        marchtime = request.form["marchtime"]
        rallytime = request.form["rallytime"]
        # default march time to 1 minute if not entered
        if not marchtime:
            marchtime = "00:01:00"
        with open(jsnfile) as rr:
            rallies = json.load(rr)
        rallies.append({"id": id, "playername": playername, "rallytarget": rallytarget, "marchtime": marchtime, "rallytime": rallytime})
        with open(jsnfile, 'w') as rw:
            json.dump(rallies, rw)
        return redirect('/')
@rallymanager.route('/updaterallylead/<string:id>',methods = ['GET','POST'])
def updaterallylead(id):
    with open(jsnfile) as rr:
        rallies = json.load(rr)
    if request.method == 'GET':
        rally = [x for x in rallies if x['id'] == id][0]
        return render_template("addrallylead.html", rally = rally)
    if request.method == 'POST':
        for rally in rallies:
            if(rally['id'] == id):
                rally['playername'] = request.form["playername"]
                rally['rallytarget'] = request.form["rallytarget"]
                rally['marchtime'] = request.form["marchtime"]
                rally['rallytime'] = request.form["rallytime"]
                # default march time to 1 minute if not entered
                if not rally['marchtime']:
                    rally['marchtime'] = "00:01:00"
                break
        with open(jsnfile, 'w') as rw:
            json.dump(rallies, rw)
        return redirect('/')
@rallymanager.route('/deleterallylead/<string:id>')
def deleterallylead(id):
    print("1111")
    with open(jsnfile) as rr:
        rallies = json.load(rr)
    newrallylist = []
    for rally in rallies:
        if(rally['id'] != id):
            newrallylist.append(rally)
    with open(jsnfile, 'w') as rw:
        json.dump(newrallylist, rw)
    return redirect('/')
@rallymanager.route("/calculate", methods = ['GET','POST'])
def calculate():
    if request.method == 'POST':
        OUTPUTTEMP = None
        OUTPUTFULL = None
        OUTPUT = None
        attacktarget = request.form["attacktarget"]
        arrivaltime = request.form["arrivaltime"]
        if not arrivaltime:
            arrivaltime = "10:00:00"
        #print("attacktarget is " + attacktarget)
        #print("arrivaltime is " + arrivaltime)

        v_arrivaltime = dt.datetime.strptime(arrivaltime,'%H:%M:%S')
        DESCRIPTION = "For rallies to arrive at " + attacktarget + " @ " + v_arrivaltime.strftime('%H:%M:%S') +"..."
        with open(jsnfile) as rr:
            rallies = json.load(rr)
        for rally in rallies:
            if rally['rallytarget'] == attacktarget:
                OUTPUTTEMP = rally['id'] + " - " + rally['playername'] + " - " + rally['marchtime'] + " - " + rally['rallytime'] + ". "
                #print(OUTPUTTEMP)
                # calculations here

                # capture values from form input
                rally_lead_name = rally['playername']
                rally_march_time = rally['marchtime']
                rally_duration = int(rally['rallytime'])
                # needed for calculation
                time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')

                # check form entries and convert
                v_rally_march_time = dt.datetime.strptime(rally_march_time,'%H:%M:%S')

                rally_start = v_arrivaltime - \
                    time_zero - \
                    timedelta(hours=v_rally_march_time.hour, minutes=v_rally_march_time.minute, seconds=v_rally_march_time.second) - \
                    timedelta(minutes=rally_duration)
                #print("rally_one_start is " + str(rally_one_start))
                OUTPUTFULLTEMP = rally_lead_name + ' start ' + str(rally_duration) + ' minute rally @ ' + str(rally_start) + '. ' 
                #print(OUTPUTFULLTEMP)

                # debug output
                if OUTPUT == None:
                    OUTPUT = OUTPUTTEMP
                else:
                    OUTPUT += OUTPUTTEMP
                # full output
                if OUTPUTFULL == None:
                    OUTPUTFULL = OUTPUTFULLTEMP
                else:
                    OUTPUTFULL += OUTPUTFULLTEMP
        # return redirect('/')
        if OUTPUTFULL == None:
            OUTPUTFULL = "Please add rally lead information to attack the " + attacktarget

        # log output
        print(DESCRIPTION + OUTPUTFULL)

        return render_template("calculate.html", attacktarget = attacktarget, arrivaltime=arrivaltime, Description = DESCRIPTION, CalculatedResult = OUTPUTFULL)
        # return render_template("calculate.html")
    if request.method == 'GET':
        return render_template("calculate.html")

if(__name__ == "__main__"):
    # development running
    rallymanager.run(host="0.0.0.0", port=3000)
    # production running
    # from waitress import serve
    # serve(rallymanager, host="0.0.0.0", port=3000)