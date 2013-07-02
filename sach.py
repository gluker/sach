from datetime import *

class Worker:

    hourly_salary = 0
    overtime_rate = 0
    overtime_hour = 0
    shabes_rate = 0
    shabes_time = 0
    param_list = []
    filename = ""
    dutys = []

    class Duty:
        date = datetime.min
        date_fin = datetime.min
        d_hour = 0
        d_min = 0
        h_s = 0
        def __str__(self):
            return self.date.strftime("%d/%m/%y %w %H:%M ")+(
                   str(self.price())+" NIS "+
                   self.date_fin.strftime("%d/%m/%y %w %H:%M "))
        
        def __init__(self, d, m, y, start_h, start_m, duration_h, duration_m,
                     hourly_salary, shabes_time, shabes_rate,
                     overtime_hour, overtime_rate):
            self.d_hour = int(duration_h)
            self.d_min = int(duration_m)
            self.hourly_salary = hourly_salary
            self.shabes_time = int(shabes_time)
            self.shabes_rate = shabes_rate
            self.overtime_hour = overtime_hour
            self.overtime_rate = overtime_rate
            self.date = datetime(y, m, d, start_h, start_m)
            self.date_fin = self.date+timedelta(hours=self.d_hour,
                                                         minutes=self.d_min)
            
            
        def isHolyday(self, date):

            if (date.weekday() == 4) and (date.hour >= self.shabes_time):
                return True
            elif (date.weekday() == 5) and (date.hour < self.shabes_time):
                return True
            else:
                return False
            
        def price(self):
            sum = 0
            sum += self.d_hour * self.hourly_salary
            sum += self.d_min * (self.hourly_salary / 60)
            if (self.d_hour >= self.overtime_hour):
                sum += self.d_min * ((self.hourly_salary *
                                      (self.overtime_rate-1)) / 60)
                sum += (self.d_hour - self.overtime_hour) * (
                        self.hourly_salary * (self.overtime_rate-1))

                
            if self.date.weekday() == 4:
                shab_start = self.date.replace(hour = int(self.shabes_time))
                shab_end = shab_start+timedelta(days=1)
            if self.date.weekday() == 5:
                shab_end = self.date.replace(hour = int(self.shabes_time))
                shab_start = shab_end+timedelta(days=-1)
            
            if self.isHolyday(self.date) and self.isHolyday(self.date_fin):
                sum *= self.shabes_rate
            elif (not self.isHolyday(self.date) and
                  self.isHolyday(self.date_fin)):
                sum += ((self.date_fin.hour - shab_start.hour) *
                            (self.hourly_salary * (self.shabes_rate - 1)))
            elif (self.isHolyday(self.date) and
                  not self.isHolyday(self.date_fin)):
                sum += ((shab_end.hour - self.date_fin.hour) *
                            (self.hourly_salary * (self.shabes_rate - 1)))
            
                     
                       
            return round(sum, 2)


    def __init__(self, data_file):
        self.filename = data_file
        param_list = []
        file = open(self.filename,'r')
        for line in file:
            if (line[0] != '#'):
                self.param_list.append(float(line))
        self.hourly_salary = self.param_list[0]
        self.overtime_rate = self.param_list[1]
        self.overtime_hour = self.param_list[2]
        self.shabes_rate = self.param_list[3]
        self.shabes_time = self.param_list[4]
                        
    def addDuty(self,d,m,y, start_h, start_m, duration_h, duration_m):
        cd = self.Duty(d, m, y, start_h, start_m, duration_h, duration_m,
                       self.hourly_salary, self.shabes_time, self.shabes_rate,
                       self.overtime_hour, self.overtime_rate)
        self.dutys.append(cd)

    def totalPrice(self):
        sum = 0
        for duty in self.dutys:
            sum += duty.price()
        return sum


iam = Worker("data.dt")
iam.addDuty(28,6,2013,14,0,8,0)
iam.addDuty(29,6,2013,14,0,8,0)
iam.addDuty(20,6,2013,6,0,8,0)
iam.addDuty(18,6,2013,6,0,8,0)
iam.addDuty(19,6,2013,6,0,12,0)
print iam.hourly_salary 
for duty in iam.dutys:
    print duty
print iam.totalPrice()

d = datetime(1,1,1)
print d.weekday()

