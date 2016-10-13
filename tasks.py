


from invoke import task

@task
def install_build_dependencies(ctx):
    ctx.run('pip install -r requirements_build.txt')

@task
def test(ctx):
    ctx.run('pytest --cov zanna')

@task
def validate(ctx):
    ctx.run('flake8 zanna')

@task(test, validate)
def build(ctx):
    pass
    
