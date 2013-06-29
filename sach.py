from datetime import *

class worker:

    hourly_salary = 0
    overtime_rate = 0
    shabes_rate = 0    
    param_list = []
    filename = ""
    dutys = []

    class duty:
        date = datetime.min
        d_hour = 0
        d_min = 0
        h_s = 0
        def __str__(self):
            return self.date.strftime("%d/%m/%y  %H:%M")+" "+str(self.date.weekday())+" "+str(self.price())+" NIS"
        def __init__(self,d,m,y,s_h,s_m,d_h,d_m,h_s):
            self.d_hour = d_h
            self.d_min = d_m
            self.h_s = h_s
            self.date = datetime(y,m,d,s_h,s_m)
        def price(self):
            sum = 0
            print self.date.weekday()
            if self.date.weekday() in (4,5):
                sum += 100
            sum += self.d_hour*self.h_s
            sum += self.d_min*(self.h_s/60)
            return round(sum,2)
        

    def __init__(self, data_file):
        self.filename = data_file
        param_list = []
        file = open(self.filename,'r')
        for line in file:
            if (line[0] != '#'):
                self.param_list.append(float(line))
        self.hourly_salary = self.param_list[0]
        self.overtime_rate = self.param_list[1]
        self.shabes_rate = self.param_list[2] 
                
        
    def addDuty(self,d,m,y,s_h,s_m,d_h,d_m):
        cd = self.duty(d,m,y,s_h,s_m,d_h,d_m,self.hourly_salary)
        self.dutys.append(cd)




iam = worker("data.dt")
iam.addDuty(29,6,2013,6,0,8,0)
iam.addDuty(20,6,2013,6,0,8,0)
iam.addDuty(18,6,2013,6,0,8,0)
iam.addDuty(19,6,2013,6,0,12,0)
print iam.hourly_salary 
for duty in iam.dutys:
    print duty


