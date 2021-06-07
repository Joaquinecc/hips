import subprocess
from utils.models import QuarentineDirectory
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