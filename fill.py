import datetime
import wx
import json

DEFAULTSTRUCT = {"dutys":[]}
FILENAME="oct14.json"
try:
    fl = open(FILENAME,'r')
    parced = json.load(fl)
    fl.close()
except IOError:
    print ("File "+FILENAME+" don't exist")
    if raw_input("Create?") != 'y':
        exit()
    parced = DEFAULTSTRUCT
while(1):
    try:
        base = float(raw_input("Hourly salary:"))
        year = int(raw_input("Year:"))
        month = int(raw_input("Month:"))
    except ValueError:
        print "Try again"
        continue
    break
while (1):
    day = (raw_input("Day:"))
    hour = (raw_input("Hour:"))
    minute = (raw_input("Minute:"))
    duration_h = (raw_input("Duration(hours):"))
    duration_m = (raw_input("Duration(minutes):"))
    try:
        date_in = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute))
        date_fin = date_in + datetime.timedelta(hours = int(duration_h),minutes = int(duration_m))
        base = float(base)
    except ValueError:
        print ("Incorrect data, try again")
        continue
    dutyJ = {"date":date_in.isoformat(),"date_fin":date_fin.isoformat(),"base":base}
    parced["dutys"].append(dutyJ)
    print dutyJ
    if raw_input("Continue?") == 'n':
        break

print parced
fl = open(FILENAME,'w+')
json.dump(parced,fl,separators=(',', ': '),indent=1)
fl.close()
