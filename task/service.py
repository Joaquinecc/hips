import subprocess
from utils.models import QuarentineDirectory,Threshold
from utils.service import  add_to_alarm_log, add_to_prevention_log


#Global Variable
threshold_fail_authentication_alarm=Threshold.objects.all().first().threshold_fail_authentication_alarm
threshold_fail_authentication_prevention=Threshold.objects.all().first().threshold_fail_authentication_prevention


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
    """
    Block ip
    """
    
    p =subprocess.Popen("iptables -I INPUT -s "+ip+" -j DROP", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    p =subprocess.Popen("service iptables save", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()



def block_user(username):
    """
    Change user shell
    """
    p =subprocess.Popen("usermod -s /sbin/nologin {}".format(username), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    return output.decode("utf-8")
def block_email(email):
    # https://stackoverflow.com/questions/492387/indentationerror-unindent-does-not-match-any-outer-indentation-level
    p =subprocess.Popen("echo \""+email+"               REJECT\">>/etc/mail/access", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p =subprocess.Popen("cd /etc/mail && ./make", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p=subprocess.Popen("systemctl restart sendmail", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()


def prevention_user(data,path):
    for username in data:
        if data[username] > threshold_fail_authentication_alarm:
            add_to_alarm_log("user:{}. {} failed login attempt. Log: {} ".format(username,data[username],path))
        if data[username] > threshold_fail_authentication_prevention:
            add_to_prevention_log("Block user:{}. {} failed login attempt. Log: {} ".format(username,data[username],path))
            block_user(username)
def prevention_ip(data,path,message='error downloading pages.'):
    for ip in data:
        if data[ip] > threshold_fail_authentication_alarm:
            add_to_alarm_log("ip:{}. {} {} . Log {} ".format(ip,data[ip],message,path))
        if data[ip] > threshold_fail_authentication_prevention:
            add_to_prevention_log("Block ip:{}. {} {} :Log {} ".format(ip,data[ip],message,path))
            block_ip(ip)
def prevention_email(data,path):
    for email in data:
        if data[email] > threshold_fail_authentication_alarm:
            add_to_alarm_log("email:{}. massive mail sent ({} email) . Log {} ".format(email,data[email],path))
        if data[email] > threshold_fail_authentication_prevention:
            add_to_prevention_log("Block email:{}. massive mail sent ({} email) . Log {} ".format(email,data[email],path))
            block_email(email)