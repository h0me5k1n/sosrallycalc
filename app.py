from flask import render_template, request
from keep_alive import keep_alive, app
import time
import datetime as dt
from datetime import timedelta

global rally_lead_one_name
global rally_one_march_time
global rally_one_duration
global rally_lead_two_name 
global rally_two_march_time 
global rally_two_duration 
global rally_lead_three_name 
global rally_three_march_time 
global rally_three_duration 
global rally_time 
global operation

def rallydurationholder():
    #reset all variables
    opselect_rally1duration1 = None
    opselect_rally1duration2 = None
    opselect_rally1duration5 = None
    opselect_rally1duration10 = None
    opselect_rally1duration15 = None
    opselect_rally2duration1 = None
    opselect_rally2duration2 = None
    opselect_rally2duration5 = None
    opselect_rally2duration10 = None
    opselect_rally2duration15 = None
    opselect_rally3duration1 = None
    opselect_rally3duration2 = None
    opselect_rally3duration5 = None
    opselect_rally3duration10 = None
    opselect_rally3duration15 = None

    if rally_one_duration == "1":
        opselect_rally1duration1 = ' selected="selected"'
    elif rally_one_duration == "2":
        opselect_rally1duration2 = ' selected="selected"'
    elif rally_one_duration == "5":
        opselect_rally1duration5 = ' selected="selected"'
    elif rally_one_duration == "10":
        opselect_rally1duration10 = ' selected="selected"'
    elif rally_one_duration == "15":
        opselect_rally1duration15 = ' selected="selected"'

    if rally_two_duration == "1":
        opselect_rally2duration1 = ' selected="selected"'
    elif rally_two_duration == "2":
        opselect_rally2duration2 = ' selected="selected"'
    elif rally_two_duration == "5":
        opselect_rally2duration5 = ' selected="selected"'
    elif rally_two_duration == "10":
        opselect_rally2duration10 = ' selected="selected"'
    elif rally_two_duration == "15":
        opselect_rally2duration15 = ' selected="selected"'

    if rally_three_duration == "1":
        opselect_rally3duration1 = ' selected="selected"'
    elif rally_three_duration == "2":
        opselect_rally3duration2 = ' selected="selected"'
    elif rally_three_duration == "5":
        opselect_rally3duration5 = ' selected="selected"'
    elif rally_three_duration == "10":
        opselect_rally3duration10 = ' selected="selected"'
    elif rally_three_duration == "15":
        opselect_rally3duration15 = ' selected="selected"'

@app.route("/")
def main():
    # set default rally time
    opselect_rally1duration5 = ' selected="selected"'
    opselect_rally2duration5 = ' selected="selected"'
    opselect_rally3duration5 = ' selected="selected"'

    return render_template("calculator.html", opselect_rally1duration5=opselect_rally1duration5, opselect_rally2duration5=opselect_rally2duration5, opselect_rally3duration5=opselect_rally3duration5)

@app.route("/calculate", methods=["POST"])
def calculate():
    # set default rally time
    opselect_rally1duration5 = ' selected="selected"'
    opselect_rally2duration5 = ' selected="selected"'
    opselect_rally3duration5 = ' selected="selected"'
    
    # capture values from form input
    rally_lead_one_name = request.form["rally_lead_one_name"]
    rally_one_march_time = request.form["rally_one_march_time"]
    rally_one_duration = int(request.form["rally_one_duration"])
    rally_lead_two_name = request.form["rally_lead_two_name"]
    rally_two_march_time = request.form["rally_two_march_time"]
    rally_two_duration = int(request.form["rally_two_duration"])
    rally_lead_three_name = request.form["rally_lead_three_name"]
    rally_three_march_time = request.form["rally_three_march_time"]
    rally_three_duration = int(request.form["rally_three_duration"])
    rally_time = request.form["rally_time"]
    operation = request.form["operation"]
    # needed for calculation
    time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')

    # check form entries and convert
    v_rally_one_march_time = dt.datetime.strptime(rally_one_march_time,'%H:%M:%S')
    v_rally_two_march_time = dt.datetime.strptime(rally_two_march_time,'%H:%M:%S')
    v_rally_three_march_time = dt.datetime.strptime(rally_three_march_time,'%H:%M:%S')
    v_rally_time = dt.datetime.strptime(rally_time,'%H:%M:%S')

    # reset variables for selected items
    opselect_fromfirstrally = None
    opselect_toarrivaltime = None

    if operation == "fromfirstrally":
        # check rally one details exist
        rally_one_start = v_rally_time - time_zero 
        #print("rally_one_start is " + str(rally_one_start))
        result1 = rally_lead_one_name + ' start ' + str(rally_one_duration) + ' minute rally @ ' + str(v_rally_time.strftime('%H:%M:%S')) + '. '

        # check rally two details exist
        rally_two_start = v_rally_time - time_zero + timedelta(hours=v_rally_one_march_time.hour, minutes=v_rally_one_march_time.minute, seconds=v_rally_one_march_time.second) - timedelta(hours=v_rally_two_march_time.hour, minutes=v_rally_two_march_time.minute, seconds=v_rally_two_march_time.second)
        #print("rally_two_start is " + str(rally_two_start))
        result2 = rally_lead_two_name + ' start ' + str(rally_two_duration) + ' minute rally @ ' + str(rally_two_start) + '. '

        # check rally three details exist
        rally_three_start = v_rally_time - time_zero + timedelta(hours=v_rally_one_march_time.hour, minutes=v_rally_one_march_time.minute, seconds=v_rally_one_march_time.second) - timedelta(hours=v_rally_three_march_time.hour, minutes=v_rally_three_march_time.minute, seconds=v_rally_three_march_time.second)
        #print("rally_three_start is " + str(rally_three_start))
        result3 = rally_lead_three_name + ' start ' + str(rally_three_duration) + ' minute rally @ ' + str(rally_three_start) + '. '

        # check rally time details exist
        #print("v_rally_time is " + v_rally_time.strftime('%H:%M:%S'))

        # set as selected operation
        opselect_fromfirstrally = ' selected="selected"'

        # generate the combined result
        description = 'for rallies to arrive at the same time when the first one starts at ' + v_rally_time.strftime('%H:%M:%S')
        result = result1 + result2 + result3
        print(result)

        return render_template("calculator.html", opselect_fromfirstrally=opselect_fromfirstrally, result=result, rally_lead_one_name=rally_lead_one_name, rally_one_march_time=rally_one_march_time, rally_lead_two_name=rally_lead_two_name, rally_two_march_time=rally_two_march_time, rally_lead_three_name=rally_lead_three_name, rally_three_march_time=rally_three_march_time, operation=operation, rally_time=rally_time, opselect_rally1duration5=opselect_rally1duration5, opselect_rally2duration5=opselect_rally2duration5, opselect_rally3duration5=opselect_rally3duration5, description=description)

    elif operation == "toarrivaltime":
        # check rally one details exist
        rally_one_start = v_rally_time - \
            time_zero - \
                timedelta(hours=v_rally_one_march_time.hour, minutes=v_rally_one_march_time.minute, seconds=v_rally_one_march_time.second) - \
                    timedelta(minutes=rally_one_duration)
        #print("rally_one_start is " + str(rally_one_start))
        result1 = rally_lead_one_name + ' start ' + str(rally_one_duration) + ' minute rally @ ' + str(rally_one_start) + '. ' 

        # check rally two details exist
        rally_two_start = v_rally_time - \
            time_zero - \
                timedelta(hours=v_rally_two_march_time.hour, minutes=v_rally_two_march_time.minute, seconds=v_rally_two_march_time.second) - \
                    timedelta(minutes=rally_two_duration)
        #print("rally_two_start is " + str(rally_two_start))
        result2 = rally_lead_two_name + ' start ' + str(rally_two_duration) + ' minute rally @ ' + str(rally_two_start) + '. '

        # check rally three details exist
        rally_three_start = v_rally_time - \
            time_zero - \
                timedelta(hours=v_rally_three_march_time.hour, minutes=v_rally_three_march_time.minute, seconds=v_rally_three_march_time.second) - \
                    timedelta(minutes=rally_three_duration)
        #print("rally_three_start is " + str(rally_three_start))
        result3 = rally_lead_three_name + ' start ' + str(rally_three_duration) + ' minute rally @ ' + str(rally_three_start) + '. '

        # check rally time details exist
        #print("v_rally_time is " + v_rally_time.strftime('%H:%M:%S'))

        # set as selected operation
        opselect_toarrivaltime = ' selected="selected"'
        
        # generate the combined result
        description = 'for rallies to arrive at ' + v_rally_time.strftime('%H:%M:%S')
        result = result1 + result2 + result3
        print(result)

        return render_template("calculator.html", opselect_toarrivaltime=opselect_toarrivaltime, result=result, rally_lead_one_name=rally_lead_one_name, rally_one_march_time=rally_one_march_time, rally_lead_two_name=rally_lead_two_name, rally_two_march_time=rally_two_march_time, rally_lead_three_name=rally_lead_three_name, rally_three_march_time=rally_three_march_time, operation=operation, rally_time=rally_time, opselect_rally1duration5=opselect_rally1duration5, opselect_rally2duration5=opselect_rally2duration5, opselect_rally3duration5=opselect_rally3duration5, description=description)

    else:
        return render_template("calculator.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html", error=error)

if __name__ == "__main__":
    keep_alive()
