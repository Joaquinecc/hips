import subprocess
from utils.models import QuarentineDirectory
def kill_process(pid):
    """
    Se recibe como parametro el pid.
    Kill al pid
    """
    p =subprocess.Popen("kill -9 "+str(pid), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

def send_to_quarentine(file_dir):
    """
    Manda un proceso un archivo a Cuarentena
    """
    path=QuarentineDirectory.objects.all()[0]
    p =subprocess.Popen("mv "+file_dir+" "+path.path, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
