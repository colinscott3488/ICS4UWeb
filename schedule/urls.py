from django.urls import path

from .views import weekChange, tableRequest, userFind, userWeek, scheduleEdit, shiftMarketList, claimShift

urlpatterns = [
    path("", tableRequest, name="table"),
    path("week_change", weekChange, name="week_change"),
    path("userfind", userFind, name="userfind"),
    path("userfound", userWeek, name="userfound"),
    path("scheduleEdit", scheduleEdit, name='scheduleEdit'),
    path("marketplace", shiftMarketList, name="marketplace"),
    path('claimshift', claimShift, name='claimshift')
]