from fabric.api import *
from fabtools import require

import fabtools

env.use_ssh_config = True
env.hosts = ['lc']
env.user = 'pi'
env.key_filename = "/home/ben/.ssh/id_rsa"


@task
def qd(comment):
    local("git add . && git commit -m \"{}\" && git push origin master".format(comment))
    with cd ('/home/pi/apps/homeautomation/'):
        run('git pull')
        sudo('service supervisord reload', use_sudo=True)

@task
def rebuild():
    with cd ('/home/pi/apps/homeautomation/'):
        run('python app.py rebuild')

@task
def deploy():
    with cd ('/home/pi/apps/homeautomation/'):
        run('git pull')

    # Require some Debian/Ubuntu packages
    require.deb.packages([
        'python-dev'
        'libpq-dev',
    ])

    # Require a supervisor process for our app
    require.supervisor.process('homeautomation',
        command='python /home/pi/apps/homeautomation/app.py',
        directory='/home/pi/apps/homeautomation/',
        user='pi'
    )

    # Require an nginx server proxying to our app
    require.nginx.proxied_site('thehughes.es',
        docroot='/home/pi/apps/homeautomation/',
        proxy_url='http://127.0.0.1:5000'
    )

     # Require a PostgreSQL server
    require.postgres.server()
    require.postgres.user('homeautomation', 'homeautomation')
    require.postgres.database('ha', 'homeautomation')

    # Setup requirements
    require.python.requirements('/home/pi/apps/homeautomation/requirements.txt')

    # Setup a daily cron task
    # fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')