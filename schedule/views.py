from django.shortcuts import render
import datetime
from .forms import NavigationForm, scheduleCreate
from django.http import HttpResponseRedirect
from .models import Schedule
import time

#global values for schedule creation
delta = 0
userList = ""
weekDate = ""
repeated = False

#schedule creation find user
def userFind(request):
    #adding variables to function to be used later
    global userList
    global weekDate
    global repeated

    #resetting values after click to schedule editor
    userList = ""
    weekDate = ""
    repeated = False

    #form handiling
    if request.method == 'POST':
        form = scheduleCreate(request.POST)
        if form.is_valid():
            userList = form.cleaned_data['users']
            weekDate = form.cleaned_data['weekStart']

            #redirects form to the actual schedule
            return HttpResponseRedirect("/design/userfound")
    else:
        #blank if blank
        form = scheduleCreate()

    #sends blank form off
    return render(request, 'schedulecreation.html', {'form': form})

#actual schedule creation part
def userWeek(request):
    #bringing date values into function
    global userList
    global weekDate
    global repeated

    #preventing future errors for no data in userfound
    if userList == "":
        return HttpResponseRedirect("/design/userfind")
    
    #all the schedule data in dicts, will be used on website html
    weekView = {0:'', 1:'', 2:'', 3:'', 4:'', 5:'', 6:''}
    dbEvent = {0:'no event', 1:'no event', 2:'no event', 3:'no event', 4:'no event', 5:'no event', 6:'no event'}
    jobCode = {0:'', 1:'', 2:'', 3:'', 4:'', 5:'', 6:''}

    # 3 nested for loop time :)
    #iterating on database and all that
    for x in dbEvent:
        #database objects made complicated on purpose 
        findTime = Schedule.objects.filter(user=userList, dateStarting=weekDate + datetime.timedelta(days=x)).values_list('startTime', "endTime")
        findJobCode = Schedule.objects.filter(user=userList, dateStarting=weekDate + datetime.timedelta(days=x)).values_list('jobCode')

        #place to dump cleaned up database when finished
        foundTime = []
        foundJobCode = ''

        # 3 for loops :) (taking database object and making readable)
        for a in findTime:
            for final in a:
                foundTime.append(final)
        for a in findJobCode:
            for final in a:
                foundJobCode = final

        #adding database to website values
        if foundJobCode:
            jobCode[x] = foundJobCode
        if foundTime:
            dbEvent[x] = foundTime[0].strftime("%-I:%M %p") + " - " + foundTime[1].strftime("%-I:%M %p")
        else:
            dbEvent[x] = "no event"

    #redirect to find page if no data
    if weekDate == "":
        return HttpResponseRedirect("/design/userfind")
    else:
        if repeated == False: # crashed page on reload without, needed for schedule editing :)
            weekDate = datetime.datetime.strptime(str(weekDate), "%Y-%m-%d")
    for x in range(0,7): #making individual dates
        weekView[x] = weekDate + datetime.timedelta(days=x)
    #html table to be displayed (fstring to put data)
    # strftime used to keep datetime object in place :)
    week = f'''
    <table border="0" cellpadding="0" cellspacing="10" class="month">
    <tr><th colspan="7" class="month">Week Starting {weekDate.strftime("%B %-d, %Y")} for {userList}</th></tr>
    <tr><td class="mon">{weekView[0].strftime("%A %b %-d")}</td><td class="tue">{weekView[1].strftime("%A %b %-d")}</td><td class="wed">{weekView[2].strftime("%A %b %-d")}</td><td class="thu">{weekView[3].strftime("%A %b %-d")}</td><td class="fri">{weekView[4].strftime("%A %b %-d")}</td><td class="sat">{weekView[5].strftime("%A %b %-d")}</td><td class="sun">{weekView[6].strftime("%A %b %-d")}</td></tr>
    <tr><td class="mon">{dbEvent[0]}</td><td class="tue">{dbEvent[1]}</td><td class="wed">{dbEvent[2]}</td><td class="thu">{dbEvent[3]}</td><td class="fri">{dbEvent[4]}</td><td class="sat">{dbEvent[5]}</td><td class="sun">{dbEvent[6]}</td></tr>
    <tr><td class="mon">{jobCode[0]}</td><td class="tue">{jobCode[1]}</td><td class="wed">{jobCode[2]}</td><td class="thu">{jobCode[3]}</td><td class="fri">{jobCode[4]}</td><td class="sat">{jobCode[5]}</td><td class="sun">{jobCode[6]}</td></tr>
    <tr class="button-container">
        <td class="monButton"><button type="button">Button 1</button></td>
        <td class="tueButton"><button type="button">Button 2</button></td>
        <td class="wedButton"><button type="button">Button 3</button></td>
        <td class="thuButton"><button type="button">Button 4</button></td>
        <td class="friButton"><button type="button">Button 5</button></td>
        <td class="satButton"><button type="button">Button 6</button></td>
        <td class="sunButton"><button type="button">Button 7</button></td>
    </tr>
    </table>
    '''
    repeated = True
    return render(request, 'scheduleuser.html', {'cal': week})

def weekChange(request):
    global delta

    if request.method == 'POST':
        form = NavigationForm(request.POST)
        if form.is_valid():
            direction = form.cleaned_data['direction']

            if direction == 'back':
                delta -= 14
                print("back")

            elif direction == 'forward':
                delta += 14
                print("forward")
            
            elif direction == 'current':
                delta = 0
                print("today")

            return HttpResponseRedirect("/design")
        
def scheduleEdit(request):
    if request.method == 'POST':
        #because im too lazy to use forms do all error handiling here
        apple = request.POST.get('start')
        print(apple)
        return HttpResponseRedirect("/design/userfound")
    
    

def tableRequest(request):
    global delta
    currentDate = datetime.datetime.now() + datetime.timedelta(days=delta)
    daysOf = {1 : "", 2 : "", 3 : "", 4 : "", 5 : "", 6 : "", 7 : "", 8 : "", 9 : "", 10 : "", 11 : "", 12 : "", 13 : "", 14 : "",}
    eventList = {1 : "no event", 2 : "no event", 3 : "no event", 4 : "no event", 5 : "no event", 6 : "no event", 7 : "no event", 8 : "no event", 9 : "no event", 10 : "no event", 11 : "no event", 12 : "no event", 13 : "no event", 14 : "no event"}
    weekdayDay = currentDate.weekday() + 1
    subNumber = weekdayDay - 1
    weekStart = daysOf[1]
    print(currentDate)
    count = 1
    for x in range(1, weekdayDay):
        daysOf[x] = (currentDate - datetime.timedelta(days=subNumber)).strftime("%d")
        subNumber -= 1
    for x in range(weekdayDay + 1, 15):
        daysOf[x] = (currentDate + datetime.timedelta(days=count)).strftime("%d")
        count += 1
    daysOf[weekdayDay] = currentDate.strftime("%d")
    if delta == 0:
        orange = '''{
        color: #0f1d9d;
        }
        '''
    else: orange = ''
    jobCode = {1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'', 8:'', 9:'', 10:'', 11:'', 12:'', 13:'', 14:''}
    hours = 0
    adjustedDTCurrent = currentDate - datetime.timedelta(days=weekdayDay)
    for x in eventList:
        findTime = Schedule.objects.filter(user=request.user.username, dateStarting=adjustedDTCurrent + datetime.timedelta(days=x)).values_list('startTime', "endTime")
        findJobCode = Schedule.objects.filter(user=request.user.username, dateStarting=adjustedDTCurrent + datetime.timedelta(days=x)).values_list('jobCode')
        foundTime = []
        foundJobCode = ''
        for a in findTime:
            for final in a:
                foundTime.append(final)
        for a in findJobCode:
            for final in a:
                foundJobCode = final
        if foundJobCode:
            jobCode[x] = foundJobCode
        if foundTime:
            hours += (float(foundTime[1].strftime("%H.%M")) - float(foundTime[0].strftime("%H.%M")))
            print(float(foundTime[1].strftime("%H.%M")) - float(foundTime[0].strftime("%H.%M")))
            eventList[x] = foundTime[0].strftime("%-I:%M %p") + " - " + foundTime[1].strftime("%-I:%M %p")
        else:
            eventList[x] = "no event"
    table = f'''
    <style>
        .{currentDate.strftime("%a").lower()} {orange}
    </style>
    <table border="0" cellpadding="0" cellspacing="10" class="month">
    <tr><th colspan="7" class="month">Week of {currentDate.strftime("%B")} {daysOf[1]}, {currentDate.strftime("%Y")}</th></tr>
    <tr><td class="mon">Monday {daysOf[1]}</td><td class="tue">Tuesday {daysOf[2]}</td><td class="wed">Wednesday {daysOf[3]}</td><td class="thu">Thursday {daysOf[4]}</td><td class="fri">Friday {daysOf[5]}</td><td class="sat">Saturday {daysOf[6]}</td><td class="sun">Sunday {daysOf[7]}</td></tr>
    <tr><td class="mon">{eventList[1]}</td><td class="tue">{eventList[2]}</td><td class="wed">{eventList[3]}</td><td class="thu">{eventList[4]}</td><td class="fri">{eventList[5]}</td><td class="sat">{eventList[6]}</td><td class="sun">{eventList[7]}</td></tr>
    <tr><td class="mon">{jobCode[1]}</td><td class="tue">{jobCode[2]}</td><td class="wed">{jobCode[3]}</td><td class="thu">{jobCode[4]}</td><td class="fri">{jobCode[5]}</td><td class="sat">{jobCode[6]}</td><td class="sun">{jobCode[7]}</td></tr>
    <tr></tr>
    <tr><td class="mon2">Monday {daysOf[8]}</td><td class="tue2">Tuesday {daysOf[9]}</td><td class="wed2">Wednesday {daysOf[10]}</td><td class="thu2">Thursday {daysOf[11]}</td><td class="fri2">Friday {daysOf[12]}</td><td class="sat2">Saturday {daysOf[13]}</td><td class="sun2">Sunday {daysOf[14]}</td></tr>
    <tr><td class="mon2">{eventList[8]}</td><td class="tue2">{eventList[9]}</td><td class="wed2">{eventList[10]}</td><td class="thu2">{eventList[11]}</td><td class="fri2">{eventList[12]}</td><td class="sat2">{eventList[13]}</td><td class="sun2">{eventList[14]}</td></tr>
    <tr><td class="mon2">{jobCode[8]}</td><td class="tue2">{jobCode[9]}</td><td class="wed2">{jobCode[10]}</td><td class="thu2">{jobCode[11]}</td><td class="fri2">{jobCode[12]}</td><td class="sat2">{jobCode[13]}</td><td class="sun2">{jobCode[14]}</td><td class="hours">{hours} hrs</td></tr>
    </table>
    '''
    return render(request, 'schedule.html', {'html_table': table})