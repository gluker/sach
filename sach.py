#!/usr/bin/python

import wx
from datetime import *
import json
import wx.grid as gridlib



def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

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
        def listView(self):
            return [self.date.strftime("%d/%m/%y"),
                    self.date.strftime("%H:%M"),
                    str(self.d_hour)+":"+str(self.d_min),
                    str(self.price())]
        def __str__(self):
            return self.date.strftime("%d/%m/%y %w %H:%M ")+(
                   str(self.price())+" NIS "+
                   self.date_fin.strftime("%d/%m/%y %w %H:%M "))

        def json_form(self):
            return json.dumps({"date":self.date,"date_fin":self.date_fin,"base":self.hourly_salary},default=date_handler)
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
                sum += ((shab_end.hour - self.date.hour) *
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
    def getDate(self,duty):
        return duty.date
    def byDate(self):
        return list(sorted(self.dutys,key=self.getDate))
    def readJSON(self,filename):
        fl = open(filename,'r')
        fload = json.load(fl)
        for duty in fload["dutys"]:
            date = datetime.strptime(duty["date"],'%Y-%m-%dT%H:%M:%S')
            date_fin = datetime.strptime(duty["date_fin"],'%Y-%m-%dT%H:%M:%S')
            delta = (date_fin - date).seconds
            d_hour = delta // 3600
            d_min = delta // 60 - d_hour*60
            self.addDuty(date.day,date.month,date.year,date.hour,date.minute,d_hour,d_min)


    def readFile(self, filename):
        fl = open(filename,'r')
        for line in fl:
            if line[0] != '#':
                tl = []
                for item in line.split():
                    tl.append(int(item))
                self.addDuty(*tl)

    def totalHours(self):
        hours = 0
        mins = 0
        for duty in self.dutys:
            hours += duty.d_hour
            mins += duty.d_min
        hours += mins / 60
        mins //= 60
        return hours,mins
    def totalBrutto(self):
        sum = 0
        for duty in self.dutys:
            sum += duty.price()
        return sum

    def getTax(self,filename):
        lst = []
        file = open(filename, 'r')
        for line in file:
            if line[0] != '#':
                lst.append(float(line))
        step = lst[0]
        brut = self.totalBrutto()
        if brut <= step:
            self.national_ins = brut * lst[1]
            self.health_ins = brut * lst[3]
        else:
            self.national_ins = ((brut - step) * lst[2]) + (step * lst[1])
            self.health_ins = ((brut - step) * lst[4]) + (step * lst[3])
        return round(self.national_ins + self.health_ins, 2)


    def dutyCount(self):
        return len(self.dutys)
class MainFrame(wx.Frame):
    class NewDutyFrame(wx.Frame):
        def __init__(self,parent):
            wx.Frame.__init__(self,parent,title="New Duty",size=(300,130))
            panel = wx.Panel(self)
            self.dateLabel = wx.StaticText(panel,id=wx.ID_ANY,label="Date")
            self.dateIn = wx.TextCtrl(panel,id=wx.ID_ANY)
            today = date.today()
            self.dateIn.ChangeValue(today.strftime("%d/%m/%Y"))
            self.dateSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.dateSizer.Add(self.dateLabel,1,wx.EXPAND)
            self.dateSizer.Add(self.dateIn,2,wx.EXPAND)

            self.timeLabel = wx.StaticText(panel,id=wx.ID_ANY,label="Time")
            self.timeIn = wx.TextCtrl(panel,id=wx.ID_ANY)
            self.dateIn.ChangeValue("14:00")
            self.timeSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.timeSizer.Add(self.timeLabel,1,wx.EXPAND)
            self.timeSizer.Add(self.timeIn,2,wx.EXPAND)

            self.durationLabel = wx.StaticText(panel,id=wx.ID_ANY,label="Duration")
            self.durationIn = wx.TextCtrl(panel,id=wx.ID_ANY)
            self.dateIn.ChangeValue("8:00")
            self.durationSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.durationSizer.Add(self.durationLabel,1,wx.EXPAND)
            self.durationSizer.Add(self.durationIn,2,wx.EXPAND)

            self.hourlyLabel = wx.StaticText(panel,id=wx.ID_ANY,label="Hourly")
            self.hourlyIn = wx.TextCtrl(panel,id=wx.ID_ANY)
            self.hourlySizer = wx.BoxSizer(wx.HORIZONTAL)
            self.hourlySizer.Add(self.hourlyLabel,1,wx.EXPAND)
            self.hourlySizer.Add(self.hourlyIn,2,wx.EXPAND)

            self.addButton = wx.Button(panel,id=wx.ID_ANY,label="Add")
            self.cancelButton = wx.Button(panel,id=wx.ID_ANY,label="Cancel")
            self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.buttonSizer.Add(self.addButton,1,wx.EXPAND)
            self.buttonSizer.Add(self.cancelButton,1,wx.EXPAND)
            self.cancelButton.Bind(wx.EVT_BUTTON,self.onCancel)
            self.addButton.Bind(wx.EVT_BUTTON,self.onAdd)

            self.addSizer = wx.BoxSizer(wx.VERTICAL)
            self.addSizer.Add(self.dateSizer,1,wx.EXPAND)
            self.addSizer.Add(self.timeSizer,1,wx.EXPAND)
            self.addSizer.Add(self.durationSizer,1,wx.EXPAND)
            self.addSizer.Add(self.hourlySizer,1,wx.EXPAND)
            self.addSizer.Add(self.buttonSizer,1,wx.EXPAND)

            panel.SetSizer(self.addSizer)
        def onAdd(self,event):
            return
        def onCancel(self,event):
            self.Close()

    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(300,500))
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        newMenuItem = fileMenu.Append(wx.NewId(), "&New\tCtrl+N", "New file")
        saveMenuItem = fileMenu.Append(wx.NewId(), "&Save\tCtrl+S", "Save")
        openMenuItem = fileMenu.Append(wx.NewId(), "&Open\tCtrl+O", "Open file")
        exitMenuItem = fileMenu.Append(wx.NewId(), "&Quit\tAlt+F4", "Exit")
        menuBar.Append(fileMenu,"&File")
        self.Bind(wx.EVT_MENU, self.onNew, newMenuItem)
        self.Bind(wx.EVT_MENU, self.onSave, saveMenuItem)
        self.Bind(wx.EVT_MENU, self.onOpen, openMenuItem)
        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
        self.SetMenuBar(menuBar)
        self.statusBar = self.CreateStatusBar()
    def createTable(self,w,h):
        panel = wx.Panel(self)
        #panel.SetBackgroundColour('#FACE8D')
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(h,w)
        self.totals = gridlib.Grid(panel)
        self.totals.CreateGrid(5,1)
        self.add = wx.Button(panel,id=wx.ID_ANY,label="Add duty")
        self.Bind(wx.EVT_BUTTON, self.onAdd,id=wx.ID_ANY)
        self.rsizer = wx.BoxSizer(wx.VERTICAL)
        self.rsizer.Add(self.totals,7,wx.EXPAND)
        self.totals.Center()
        self.rsizer.Add(self.add,1,wx.EXPAND)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.grid,1,wx.EXPAND)
        self.sizer.Add(self.rsizer,0,wx.EXPAND)
        panel.SetSizer(self.sizer)
    def onAdd(self,event):
        addframe = self.NewDutyFrame(self)
        addframe.Show()
    def onSave(self,event):
        if wx.MessageBox("Rewrite current file?","Confirm",wx.ICON_QUESTION | wx.YES_NO,self)==wx.NO:

            return
        return
    def onNew(self,event):
        return
    def onExit(self,event):
        self.Close()
    def onOpen(self,event):
        openFileDialog = wx.FileDialog(self,"Open JSON file","","","JSON files (*.json)|*.json",wx.FD_OPEN | wx.FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        try:
            global iam
            iam.readJSON(openFileDialog.GetPath())
            self.createTable(4,0)
            self.loadTable(iam.byDate())
            global frame
            self.sizer.Fit(frame)
            self.statusBar.SetStatusText("Brutto:"+str(iam.totalBrutto()))
        except Exception as e:
            print (e)
            print ("Error reading file")


    def loadTable(self,table):
        for i in range(len(table)):
            self.grid.AppendRows(1)
            for j in range(len(table[0].listView())):
                self.grid.SetCellValue(i,j,table[i].listView()[j])
        self.totals.SetRowLabelValue(0,"Total hours")
        self.totals.SetCellValue(0,0,str(iam.totalHours()))
        self.totals.SetRowLabelValue(1,"Brutto")
        self.totals.SetCellValue(1,0,str(iam.totalBrutto()))
        self.totals.SetRowLabelValue(2,"BTL")
        self.totals.SetRowLabelValue(3,"Health tax")
        self.totals.SetRowLabelValue(4,"Netto")
        self.totals.AutoSize()
        self.grid.SetColLabelValue(0,"Date")
        self.grid.SetColLabelValue(1,"Time")
        self.grid.SetColLabelValue(2,"Duration")
        self.grid.SetColLabelValue(3,"Total")
        self.grid.AutoSize()
        global frame
        frame.Refresh()
        self.grid.SetRowLabelSize(0)
iam = Worker("data.dt")
app = wx.App(False)
frame = MainFrame(None,"Salary counter")
frame.Show()
app.MainLoop()


