from invoke import task
import os

@task
def requestcode():
    os.system('./whatsapp_daemon/yowsup-bash-requestcode.sh')

@task
def whatsapp_daemon():
    os.system('python ./whatsapp_daemon/run.py')
