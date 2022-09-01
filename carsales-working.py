
from flask import Flask, render_template, json, request, redirect

carsales = Flask(__name__)
carsales.debug = True
jsnfile = 'carslist.json'

@carsales.route("/")
def main():
    with open(jsnfile) as cr:
        cars = json.load(cr)
    return render_template("carslist.html", cars = cars)
@carsales.route("/refresh", methods = ['GET'])
def refresh():
    return redirect('/')
@carsales.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html", car = {})
    if request.method == 'POST':
        id = request.form["playername"] + "-" + request.form["rallytarget"]
        #id = request.form["playername"]
        playername = request.form["playername"]
        rallytarget = request.form["rallytarget"]
        marchtime = request.form["marchtime"]
        rallytime = request.form["rallytime"]
        with open(jsnfile) as cr:
            cars = json.load(cr)
        cars.append({"id": id, "playername": playername, "rallytarget": rallytarget, "marchtime": marchtime, "rallytime": rallytime})
        with open(jsnfile, 'w') as cw:
            json.dump(cars, cw)
        return redirect('/')
@carsales.route('/updatecar/<string:id>',methods = ['GET','POST'])
def updatecar(id):
    with open(jsnfile) as cr:
        cars = json.load(cr)
    if request.method == 'GET':
        car = [x for x in cars if x['id'] == id][0]
        return render_template("addcar.html", car = car)
    if request.method == 'POST':
        for car in cars:
            if(car['id'] == id):
                car['playername'] = request.form["playername"]
                car['rallytarget'] = request.form["rallytarget"]
                car['marchtime'] = request.form["marchtime"]
                car['rallytime'] = request.form["rallytime"]
                break
        with open(jsnfile, 'w') as cw:
            json.dump(cars, cw)
        return redirect('/')
@carsales.route('/deletecar/<string:id>')
def deletecar(id):
    print("1111")
    with open(jsnfile) as cr:
        cars = json.load(cr)
    newcarlist = []
    for car in cars:
        if(car['id'] != id):
            newcarlist.append(car)
    with open(jsnfile, 'w') as cw:
        json.dump(newcarlist, cw)
    return redirect('/')
@carsales.route("/calculate", methods = ['GET','POST'])
def calculate():
    if request.method == 'POST':
        OUTPUTTEMP = None
        OUTPUT = None
        attacktarget = request.form["attacktarget"]
        arrivaltime = request.form["arrivaltime"]
        print("attacktarget is " + attacktarget)
        print("arrivaltime is " + arrivaltime)
        with open(jsnfile) as cr:
            cars = json.load(cr)
        for car in cars:
            if car['rallytarget'] == attacktarget:
                OUTPUTTEMP = car['id'] + " - " + car['playername'] + " - " + car['marchtime'] + " - " + car['rallytime'] + ". "
                print(OUTPUTTEMP)
                # calculations here
                
                if OUTPUT == None:
                    OUTPUT = OUTPUTTEMP
                else:
                    OUTPUT += OUTPUTTEMP
        # return redirect('/')

        return render_template("calculate.html", attacktarget = attacktarget, arrivaltime=arrivaltime, testvar = OUTPUT)
        # return render_template("calculate.html")
    if request.method == 'GET':
        return render_template("calculate.html")


if(__name__ == "__main__"):
    carsales.run()