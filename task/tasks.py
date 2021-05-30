import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import hashlib
from celery import shared_task
from  .models import HashFile,WhiteListUser
from utils.service import  add_to_alarm_log
import subprocess
from utils.models import PromiscuoDirectory
@shared_task
def verify_file_hash():
    """
    Comparamos los hash cargado en la base datos
    """
    hash_file_array=HashFile.objects.all()
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
    white_list_username = WhiteListUser.objects.all()
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
    path=PromiscuoDirectory.objects.all()[0].path
    command_log=subprocess.Popen("cat "+path+" | grep \"left promisc\"", stdout=subprocess.PIPE, shell=True)
    (output_off, err) = command_log.communicate()
    data= output_off.decode("utf-8").split('\n')
    data.pop() # Last element is just an empty string
    for line in data:
        add_to_alarm_log("Detect Device on promisco mode: {} ".format(line)) 
    