# coding=utf-8
from fabric.context_managers import cd, prefix
from fabric.decorators import task
from fabric.operations import run, local, os
from fabric.state import env

prj = {
    'root': '/home/lmdb/lmdb/',
    'src': '/home/lmdb/lmdb/'
}

@task
def prod():
    env.hosts = ['root@geconn.ru']


@task
def pull():
    with cd(prj['root']):
        run("git pull origin master")


def fcgiserver(action):
    with cd(prj['root']):
        with prefix('workon lmdb'):
            run("./server.sh %s" % action)


@task
def backup_db():
    with cd(prj['root'] + "\sql"):
        run("pg_dump -U lanit --no-owner --clean --file=full_backup.sql")
        run("gzip full_backup.sql")
    local("scp %s:%s/full_backup.sql.gz ../sql" % (env['host_string'], os.path.join(prj['root'], "sql")))


@task
def restore_db():
    local("psql -U lanit < ../sql/full_backup.sql")

@task
def collectstatic():
    with cd(prj['src']):
        with prefix('workon lmdb'):
            run("python manage.py collectstatic --noinput")

@task
def migrate():
    with cd(prj['src']):
        with prefix('workon lmdb'):
            run("python manage.py migrate")
            run("python manage.py syncdb --all")

@task
def deploy():
    pull()
    collectstatic()
    migrate()
    fcgiserver('restart')