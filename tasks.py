


from invoke import task

@task
def test(ctx):
    ctx.run('pytest')


@task(test)
def build(ctx):
    pass
    
