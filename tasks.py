from invoke import task

@task
def requestcode(c, docs=False):
    c.run('./yowsup-bash-requestcode.sh')
