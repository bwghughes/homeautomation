from fabric.api import *
from fabtools import require
import fabtools

@task
def setup():
    # Require a supervisor process for our app
    require.supervisor.process('myapp',
        command='/home/myuser/env/bin/gunicorn_paster /home/myuser/env/myapp/production.ini',
        directory='/home/myuser/env/myapp',
        user='myuser'
        )

    # Require an nginx server proxying to our app
    require.nginx.proxied_site('thehughes.es',
        docroot='/home/pi/env/myapp/myapp/public',
        proxy_url='http://127.0.0.1:8888'
        )

    # Setup a daily cron task
    fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')