def send_email_to_admin(text:str):
    f=open('testlog.txt','a')
    f.write(text )
    f.close()