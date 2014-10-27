import datetime
import json
FILENAME="ndutys.json"
fl = open(FILENAME,'r')
parced = json.load(fl)
fl.close()

base = float(raw_input("base:"))
year = int(raw_input("Year:"))
month = int(raw_input("Month:"))
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
fl = open(FILENAME,'w')
json.dump(parced,fl,separators=(',', ': '),indent=1)
fl.close()
