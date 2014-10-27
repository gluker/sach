import datetime
import json
FILENAME="dutys.json"
def readFile(self, filename):
    fl = open(filename,'r')
    for line in fl:
        if line[0] != '#':
            tl = []
            for item in line.split():
                tl.append(int(item))
            self.addDuty(*tl)

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
def tojson(d,m,y,start_h,start_m,duration_h,duration_m):
    date_in = datetime.datetime(y,m,d,start_h,start_m)
    return json.dumps({"date_in":date_in},  default=date_handler)
fl = open(FILENAME,'a')

while (1):


print tojson(1,10,2014,22,0,8,0)
