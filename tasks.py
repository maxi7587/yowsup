from invoke import task

@task
def requestcode(c, docs=False):
    c.run('./whatsapp_daemon/yowsup-bash-requestcode.sh')

@task
def whatsapp_daemon(c, docs=False):
    c.run('python ./whatsapp_daemon/run.py')
