from .models import AlarmLogDirectory,AlarmLog
import datetime
def add_to_alarm_log(text : str, ip=''):
    timestamp=str(datetime.datetime.now())
    reason="{} : Reason : {}.{}".format(timestamp,text,ip)
    new_log_reason=AlarmLog(reason=reason)
    new_log_reason.save()
    try:
        path=AlarmLogDirectory.objects.all()[0].path
        f=open(path,'a')
        f.write(reason)
    except:
        print("Not able to open alarm.log")