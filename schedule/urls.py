from django.urls import path

from .views import weekChange, tableRequest, userFind, userWeek, scheduleEdit

urlpatterns = [
    path("", tableRequest, name="table"),
    path("week_change", weekChange, name="week_change"),
    path("userfind", userFind, name="userfind"),
    path("userfound", userWeek, name="userfound"),
    path("scheduleEdit", scheduleEdit, name='scheduleEdit')
]