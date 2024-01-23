from django.shortcuts import render
import datetime
from .forms import NavigationForm, scheduleCreate
from django.http import HttpResponseRedirect
from .models import Schedule, ShiftMarketplace
import time
import random
import pyowm

owm = pyowm.OWM('bab2e151773e426c2c44c37b35bc2b01')
weather_mgr = owm.weather_manager()
place = 'Kolkata, IN'
observation = weather_mgr.weather_at_place(place)

def homePage(request):
    form = "form"
    return render(request, 'home.html', {'form': form})

#schedule creation find user
def userFind(request):
    #resetting values after click to schedule editor
    request.session['userList'] = ""
    request.session['weekDate'] = ""
    request.session['repeated'] = False

    #form handiling
    if request.method == 'POST':
        form = scheduleCreate(request.POST)
        if form.is_valid():
            request.session['userList'] = form.cleaned_data['users'].username
            request.session['weekDate'] = form.cleaned_data['weekStart'].isoformat()

            #redirects form to the actual schedule
            return HttpResponseRedirect("/design/userfound")
    else:
        #blank if blank
        form = scheduleCreate()

    #sends blank form off
    return render(request, 'schedulecreation.html', {'form': form})

#actual schedule creation part
def userWeek(request):
    #preventing future errors for no data in userfound
    if request.session['userList'] == "":
        return HttpResponseRedirect("/design/userfind")
    
    #all the schedule data in dicts, will be used on website html
    weekView = {0:'', 1:'', 2:'', 3:'', 4:'', 5:'', 6:''}
    dbEvent = {0:'no event', 1:'no event', 2:'no event', 3:'no event', 4:'no event', 5:'no event', 6:'no event'}
    jobCode = {0:'', 1:'', 2:'', 3:'', 4:'', 5:'', 6:''}

    sessionToDateTime = datetime.datetime.strptime(request.session['weekDate'], '%Y-%m-%d')

    # 3 nested for loop time :)
    #iterating on database and all that
    for x in dbEvent:
        #database objects made complicated on purpose 
        findTime = Schedule.objects.filter(user=request.session['userList'], dateStarting=sessionToDateTime + datetime.timedelta(days=x)).values_list('startTime', "endTime")
        findJobCode = Schedule.objects.filter(user=request.session['userList'], dateStarting=sessionToDateTime + datetime.timedelta(days=x)).values_list('jobCode')

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
    if request.session['weekDate'] == "":
        return HttpResponseRedirect("/design/userfind")
    else:
        if request.session['repeated'] == False: # crashed page on reload without, needed for schedule editing :)
            sessionToDateTime = datetime.datetime.strptime(request.session['weekDate'], "%Y-%m-%d")
    for x in range(0,7): #making individual dates
        weekView[x] = sessionToDateTime + datetime.timedelta(days=x)
    #html table to be displayed (fstring to put data)
    # strftime used to keep datetime object in place :)
    week = f'''
    <table border="0" cellpadding="0" cellspacing="10" class="month">
    <tr><th colspan="7" class="month">Week Starting {sessionToDateTime.strftime("%B %-d, %Y")} for {request.session['userList']}</th></tr>
    <tr><td class="mon">{weekView[0].strftime("%A %b %-d")}</td><td class="tue">{weekView[1].strftime("%A %b %-d")}</td><td class="wed">{weekView[2].strftime("%A %b %-d")}</td><td class="thu">{weekView[3].strftime("%A %b %-d")}</td><td class="fri">{weekView[4].strftime("%A %b %-d")}</td><td class="sat">{weekView[5].strftime("%A %b %-d")}</td><td class="sun">{weekView[6].strftime("%A %b %-d")}</td></tr>
    <tr><td class="mon">{dbEvent[0]}</td><td class="tue">{dbEvent[1]}</td><td class="wed">{dbEvent[2]}</td><td class="thu">{dbEvent[3]}</td><td class="fri">{dbEvent[4]}</td><td class="sat">{dbEvent[5]}</td><td class="sun">{dbEvent[6]}</td></tr>
    <tr><td class="mon">{jobCode[0]}</td><td class="tue">{jobCode[1]}</td><td class="wed">{jobCode[2]}</td><td class="thu">{jobCode[3]}</td><td class="fri">{jobCode[4]}</td><td class="sat">{jobCode[5]}</td><td class="sun">{jobCode[6]}</td></tr>
    '''
    request.session['repeated'] = True
    return render(request, 'scheduleuser.html', {'cal': week})

def shiftMarketList(request):
    items = ShiftMarketplace.objects.all()
    return render(request, 'marketplace.html', {'items': items})

#this is a brute force original number finder, this is so that
#claim shift can find the shift using just an int
def jobGener():
    while(True):
        apple = True
        num = random.randint(1, 99999999999)
        foundNum = ShiftMarketplace.objects.filter(shiftID=num)
        for x in foundNum:
            apple = False
        if apple:
            return num


def claimShift(request):
    if request.method == 'POST':
        shift = request.POST.get('shift')
        dataShift = ShiftMarketplace.objects.filter(shiftID=shift) #there cannot be duplicates
        for x in dataShift:
            findScheduled = Schedule.objects.filter(dateStarting=x.dateStarting, user=request.user.username)
            for x in findScheduled:
                return HttpResponseRedirect("/shiftclaimerror")
            addShift = Schedule()
            addShift.user = request.user.username
            addShift.dateStarting = x.dateStarting
            addShift.startTime = x.startTime
            addShift.endTime = x.endTime
            addShift.jobCode = x.jobCode
            addShift.save()
            x.delete()
            return HttpResponseRedirect("/design/marketplace")
        print(shift)
    return HttpResponseRedirect("/shiftclaimerror")

def weekChange(request):
    # delta = request.session['delta']

    if request.method == 'POST':
        form = NavigationForm(request.POST)
        if form.is_valid():
            direction = form.cleaned_data['direction']
            request.session['repeatedSched'] = True
            if direction == 'back':
                request.session['delta'] -= 14
                print("back")

            elif direction == 'forward':
                request.session['delta'] += 14
                print("forward")
            
            elif direction == 'current':
                request.session['delta'] = 0
                print("today")

            return HttpResponseRedirect("/design")
        
def scheduleEdit(request):
    if request.method == 'POST':
        #because im too lazy to use forms do all error handiling here
        startShift = request.POST.get('start')
        endShift = request.POST.get('end')
        selectedJob = request.POST.get('job')
        daySelected = request.POST.get('dayval')
        sessionToDateTime = datetime.datetime.strptime(request.session['weekDate'], '%Y-%m-%d')
        # print("Start: ", startTime, "End: ", endTime, "Selected Job: ", selectedJob) debug line
        selectedShift = Schedule.objects.filter(user=request.session['userList'], dateStarting=sessionToDateTime + datetime.timedelta(days=int(daySelected)))
        if startShift == '' and endShift == '' and selectedJob == '':
            for x in selectedShift:
                if x.jobCode == "called off":
                    return HttpResponseRedirect("/design/userfound")
                addMarketplace = ShiftMarketplace()
                addMarketplace.jobCode = x.jobCode
                addMarketplace.startTime = x.startTime
                addMarketplace.endTime = x.endTime
                addMarketplace.dateStarting = x.dateStarting
                addMarketplace.shiftID = jobGener() #randomly assigns number, so shift can be called later
                addMarketplace.save()
                print(x.jobCode)
                x.jobCode = "called off" 
                x.save()
        elif startShift != '' and endShift != '' and selectedJob != '':
            if selectedShift:
                for x in selectedShift:
                    x.startTime = datetime.datetime.strptime(startShift, "%H:%M")
                    x.endTime = datetime.datetime.strptime(endShift, "%H:%M")
                    x.dateStarting = sessionToDateTime + datetime.timedelta(days=int(daySelected))
                    x.jobCode = selectedJob
                    x.save()
            else:
                newshift = Schedule()
                newshift.user = request.session['userList']
                newshift.startTime = datetime.datetime.strptime(startShift, "%H:%M")
                newshift.endTime = datetime.datetime.strptime(endShift, "%H:%M")
                newshift.dateStarting = sessionToDateTime + datetime.timedelta(days=int(daySelected))
                newshift.jobCode = selectedJob
                newshift.save()
        else:
            HttpResponseRedirect("/design/userfound")

        return HttpResponseRedirect("/design/userfound")
    
    

def tableRequest(request):
    if "delta" not in request.session:
        request.session['delta'] = 0
    currentDate = datetime.datetime.now() + datetime.timedelta(days=request.session['delta'])
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
    if request.session['delta'] == 0:
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
    hours = (float(int(hours*100)))/100
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