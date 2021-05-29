import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import hashlib
from celery import shared_task
from  .models import HashFile
from utils.service import  add_to_alarm_log
@shared_task
def verify_file_hash():
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