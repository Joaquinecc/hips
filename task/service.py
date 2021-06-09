import subprocess
from utils.models import QuarentineDirectory
from utils.service import  add_to_alarm_log, add_to_prevention_log


#Global Variable
threshold_fail_authentication_alarm=1
threshold_fail_authentication_prevention=1


def kill_process(pid):
    """
    Se recibe como parametro el pid del processo.
    Kill al pid
    """
    p =subprocess.Popen("kill -9 "+str(pid), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

def send_to_quarentine(file_dir):
    """
    Manda archivo a la carpeta cuaretena.
    """
    path=QuarentineDirectory.objects.all()[0]
    p =subprocess.Popen("mv "+file_dir+" "+path.path, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

def block_ip(ip):
    pass
def block_user(username):
    pass

def prevention_smpt_log_service(data,path):
    for username in data:
        if data[username] > threshold_fail_authentication_alarm:
            add_to_alarm_log("user:{}. {} failed login attempt. Log: {} ".format(username,data[username],path))
        if data[username] > threshold_fail_authentication_prevention:
            add_to_prevention_log("Block user:{}. {} failed login attempt. Log: {} ".format(username,data[username],path))
            block_user(username)