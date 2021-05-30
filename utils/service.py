from .models import AlarmLogDirectory,AlarmLog,PreventionLog,PrevetionLogDirectory
import datetime
def add_to_alarm_log(text : str, ip=''):
    timestamp=str(datetime.datetime.now())
    reason="{} : Reason : {}.{}. \n".format(timestamp,text,ip)
    new_log_reason=AlarmLog(reason=reason)
    new_log_reason.save()
    try:
        path=AlarmLogDirectory.objects.all()[0].path
        f=open(path,'a')
        f.write(reason)
    except:
        print("Not able to open alarm.log")

def add_to_prevention_log(text : str, ip=''):
    timestamp=str(datetime.datetime.now())
    reason="{} : Reason : {}.{}. \n".format(timestamp,text,ip)
    new_log_reason=PreventionLog(reason=reason)
    new_log_reason.save()
    try:
        path=PrevetionLogDirectory.objects.all()[0].path
        f=open(path,'a')
        f.write(reason)
    except:
        print("Not able to open {}".format(path))