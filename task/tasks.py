import hashlib
from os import utime
from celery import shared_task
from  task import models
from utils.service import  add_to_alarm_log, add_to_prevention_log
import subprocess
from utils.models import PromiscuoDirectory,SecureLogDirectory,MessageLogDirectory,HttpAccesLogDirectory
from .service import kill_process,send_to_quarentine,block_user,prevention_user,prevention_ip_accces_log
import datetime

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
    path=MessageLogDirectory.objects.all()[0].path
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
    path=HttpAccesLogDirectory.objects.all()[0].path
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
    

