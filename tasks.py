from invoke import task

@task
def requestcode(c, docs=False):
    c.run('./yowsup-bash-requestcode.sh')

@task
def register(c, docs=False):
    c.run('./yowsup-bash-register.sh')
