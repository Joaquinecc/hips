import hashlib
from os import utime
from celery import shared_task
from  task import models
from utils.service import  add_to_alarm_log, add_to_prevention_log
import subprocess
from utils.models import PromiscuoDirectory,SecureLogDirectory,MessageLogDirectory,HttpAccesLogDirectory,MailLogDirectory,MailQueueLimit
from utils import models as umodels
from .service import kill_process,send_to_quarentine,block_user,prevention_user,prevention_ip_accces_log,prevention_email
import datetime
import psutil

@shared_task
def verify_file_hash():
    """
    Comparamos los hash cargado en la base datos
    """
    hash_file_array=models.HashFile.objects.all()
    for file in hash_file_array:
        try:
            path=file.path_file
            a_file = open(path, "rb")
            original_hash=file.hash
            content = a_file.read()
            a_file.close()
            digest = hashlib.md5(content).hexdigest()
            if digest != original_hash:
                add_to_alarm_log("File : {} was modified".format(path))
        except:
            continue
@shared_task
def check_username():
    """
    Verificamos que los ultimos accesos al sistema sean usuarios que estan en la lista blanca
    En caso contrario enviamos una alaram
    """
    command_get_user= subprocess.Popen("w -i 2>/dev/null", stdout=subprocess.PIPE, shell=True)
    (output, err) = command_get_user.communicate()
    text_line_input=output.decode("utf-8").split('\n')
    white_list_username = models.WhiteListUser.objects.all()
    #removing  from the queue unnecesary data
    text_line_input.pop(0) #Extra data
    text_line_input.pop(0)#Columns name
    text_line_input.pop() # Last element is just an empty string

    for line in text_line_input:
        data=line.split()
        username_to_check=data[0]
        match=False
        for user in white_list_username:
            if user.username == username_to_check:
                match=True
        if match != True: #The user is no on the white list
           add_to_alarm_log("Suspicious user was logged  ->{} ".format(line)) 
@shared_task
def check_log_promicuo():
    """
    Verificamos el archivo log para identificar si una interfaz esta en modo promiscuo
    """
    path=PromiscuoDirectory.objects.all()[0].path
    command_log=subprocess.Popen("cat "+path+" | grep -i promis ", stdout=subprocess.PIPE, shell=True)
    (output, err) = command_log.communicate()
    data= output.decode("utf-8").split('\n')
    data.pop() # Last element is just an empty string
    for line in data:
        add_to_alarm_log("Detect Device on promisco mode: {} ".format(line)) 

@shared_task
def check_promisc_app():
    """
    Verificamos que las app en la lista negra no se esten ejecutando. Si se encuentra se elimina
    """
    apps=models.BlackListApp.objects.all()
    for app in apps:
        name=app.app
        command=subprocess.Popen("ps aux | grep -i "+name+" | grep -v grep", stdout=subprocess.PIPE, shell=True)
        (output, err) = command.communicate()
        data_string= output.decode("utf-8")
        if data_string == '': #No match
            continue
        add_to_alarm_log("App {} was found .  Log Result: -- \n{} \n -- ".format(name,data_string))

        #Prevention
        data= data_string.split('\n')
        data.pop() # Last element is just an empty string.
        for d in data:
            line=d.split()
            pid=line[1]
            file_dir=line[-1]
            kill_process(pid)
            send_to_quarentine(file_dir)

@shared_task
def check_fail_auth_log_secure_smpt():
    """
    Look at the secure log if there was a multiple failed login attempt
        """

    path=SecureLogDirectory.objects.all()[0].path
    temp = datetime.datetime.now()
    date =temp.strftime("%b  %-d")
    command=subprocess.Popen("grep -i "+'"'+ date+'"' +" " +path+ " | grep -i \"authentication failure\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = command.communicate()
    data_string= output.decode("utf-8")
    data=data_string.split("\n")
    data.pop() #Last element is just an empty string.
    user_failed_count={}
    for line in data:
        username = line.split()[-1].replace("user=","")
        user_failed_count[username]= 1 if username not in user_failed_count  else user_failed_count[username]+1
    prevention_user(user_failed_count,path)

    
@shared_task
def check_fail_auth_log_messages_smpt():
    """
    Look at the secure log if there was a multiple failed login attempt
        """    
    path=MessageLogDirectory.objects.all().first().path
    temp = datetime.datetime.now()
    date =temp.strftime("%b  %-d")
    command=subprocess.Popen("grep -i "+'"'+ date+'"' +" " +path+ " | grep -i \"service=smtp\" |  grep -i \"auth failure\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = command.communicate()
    data_string= output.decode("utf-8")
    data=data_string.split("\n") 
    data.pop() #Last element is just an empty string.
    user_failed_count={}
    for line in data:
        username = line.split()[9].replace("[user=","").replace(']',"")
        user_failed_count[username]= 1 if username not in user_failed_count  else user_failed_count[username]+1
    prevention_user(user_failed_count,path)

@shared_task
def check_acces_log():
    """
    Look at the secure log if there was a multiple failed login attempt
        """  
    path=HttpAccesLogDirectory.objects.all().first().path
    temp = datetime.datetime.now()
    date =temp.strftime("%-d/%b/%Y")
    command=subprocess.Popen("grep -i "+'"'+ date+'"' +" " +path+ " | grep -i 404", stdout=subprocess.PIPE, shell=True)
    (output, err) = command.communicate()
    data_string= output.decode("utf-8")
    data=data_string.split("\n") 
    data.pop() #Last element is just an empty string.
    ip_count={}
    for line in data:
        ip = line.split()[0]
        ip_count[ip]= 1 if ip not in ip_count  else ip_count[ip]+1
    prevention_ip_accces_log(ip_count,path) 
    
@shared_task
def check_mailog():
    """
    Look at the mailo log to check multiple email sent in a shor period time by a user
        """  
    path=MailLogDirectory.objects.all().first().path
    temp = datetime.datetime.now()
    date =temp.strftime("%b  %-d")
    command=subprocess.Popen("grep -i "+'"'+ date+'"' +" " +path+ " | grep -i \"from=<\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = command.communicate()
    data_string= output.decode("utf-8")
    data=data_string.split("\n") 
    data.pop() #Last element is just an empty string.
    email_acount_counter={}
    for line in data:
        email = line.split()[6].replace("from=<",'').replace(">,",'')
        email_acount_counter[email]= 1 if email not in email_acount_counter  else email_acount_counter[email]+1
    prevention_email(email_acount_counter,path) 
@shared_task
def check_mail_queue():
    limit = MailQueueLimit.objects.all().first().qty
    command=subprocess.Popen("mailq", stdout=subprocess.PIPE, shell=True)
    (output, err) = command.communicate()
    data= output.decode("utf-8").split('\n')
    if len(data) > limit:
        pass

@shared_task
def check_consume_process():
    treshold=umodels.ProcessConsumeLimit.objects.all.first()
    max_cpu=treshold.max_cpu
    max_ram=treshold.max_ram
    for proc in psutil.process_iter(['pid',"name",'cpu_percent','memory_percent']):
        if(proc.info['cpu_percent'] > max_cpu or  proc.info['memory_percent'] > max_ram ):
            add_to_alarm_log("process {} with pid {}  cpu_percent:{} memory_percent:{} \n ".format(proc.info['name'],proc.info['pid']),proc.info['cpu_percent'], max_cpu,proc.info['memory_percent'] )
            add_to_prevention_log("Kill process {} with pid {}  cpu_percent:{} memory_percent:{} \n ".format(proc.info['name'],proc.info['pid']),proc.info['cpu_percent'], max_cpu,proc.info['memory_percent'] )
            kill_process(proc.info['pid'])

@shared_task
def check_tmp_directory():
    for endpoint in umodels.ScriptType.objects.all():
        command=subprocess.Popen("ls /tmp/*.{}".format(endpoint), stdout=subprocess.PIPE, shell=True)
        (output, err) = command.communicate()
        for file in output.decode("utf-8").split('\n'):
            add_to_alarm_log("Found file {}  inside folder /tmp".format(file))
            add_to_prevention_log("Send to quarantine file {} found inside folder /tmp".format(file))
            send_to_quarentine("/tmp/{}".format(file))
@shared_task
def check_cronjobs():
    for endpoint in umodels.ScriptType.objects.all():
        command=subprocess.Popen("crontab -l | grep .{}".format(endpoint), stdout=subprocess.PIPE, shell=True)
        (output, err) = command.communicate()
        data= output.decode("utf-8")
        if data:
            add_to_alarm_log("Found script type {} on crontab list.\n Log: \n {}".format(endpoint,data))



    