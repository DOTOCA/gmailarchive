import dodo
from fabric.api import *
from fabric.operations import *
from fabric.colors import green as _green
from fabric.colors import yellow as _yellow
from fabric.colors import red as _red
from fabric.contrib.files import *
import os.path
import sys
import time

env.project_name = 'gmailarchive'
droplet_name = 'gmailarchive'

def _always_run():
    print 'ALWAYS RUNNING'

def _dodo_servers():
    droplets = [d for d in conn.droplets() if d['name'] == droplet_name]
    return droplets

def dodo_create_server():
    conn = dodo.connect()
    conn.new_droplet(droplet_name, size_id, 25306, 1, 4648)

def dodo_start_server():

    conn = dodo.connect()
    droplets = _dodo_servers()

    dodo_create_server()

    while len(droplets) < 0:
        time.sleep(5)
        droplets = _dodo_servers()



_always_run()
